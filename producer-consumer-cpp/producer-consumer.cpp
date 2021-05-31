#include <algorithm>
#include <cctype>
#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>

template <class T>
class SynchronizedQueue {
  public:
    void Push(T value) {
      std::lock_guard<std::mutex> lock(mutex_);
      bool wake = queue_.empty();
      queue_.push(value);
      if (wake) cv_.notify_one();
    }

    T Pop() {
      std::unique_lock<std::mutex> unique_lock(mutex_);
      while (queue_.empty()) cv_.wait(unique_lock);
      T value = queue_.front(); queue_.pop();
      return value;
    }

  private:
    std::queue<T> queue_;
    std::mutex mutex_;
    std::condition_variable cv_;
};

SynchronizedQueue<std::string> PRODUCER_QUEUE, CONSUMER_QUEUE;

void produce() {
  std::string line;
  while (getline(std::cin, line)) {
    PRODUCER_QUEUE.Push(line);
  }
}

void handle() {
  while (true) {
    std::string line = PRODUCER_QUEUE.Pop();
    std::transform(line.begin(), line.end(), line.begin(),
                   [] (unsigned char c) { return std::tolower(c); });
    CONSUMER_QUEUE.Push(line);
  }
}

void consume() {
  while (true) {
    std::string line = CONSUMER_QUEUE.Pop();
    std::cout << line << "\n";
  }
}

int main() {
  std::freopen("Shakespeares-Sonnets.txt", "r", stdin);
  std::freopen("shakespeares-sonnets-lowercase.txt", "w", stdout);

  std::thread producer(produce), handler(handle), consumer(consume);
  producer.join(), handler.detach(), consumer.detach();
  std::this_thread::sleep_for(std::chrono::seconds(1));

  return 0;
}
