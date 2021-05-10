#include <atomic>
#include <chrono>
#include <deque>
#include <iostream>
#include <mutex>
#include <random>
#include <string>
#include <thread>

std::mutex cout_mutex;

struct Chopstick {
  std::mutex mutex;
};

struct DiningTable {
  std::atomic<bool> ready{false};
  std::deque<Chopstick> chopsticks;
  explicit DiningTable(int size);
};

class Philosopher {
  public:
    Philosopher(int index, const DiningTable& table, Chopstick& left, Chopstick& right);
    void Dine();
    ~Philosopher();

  private:
    const int index_;
    std::thread thread_;
    Chopstick &left_, &right_;
    const DiningTable& dining_table_;
    std::mt19937 generator_{std::random_device{}()};

    void Eat();
    void Talk();
    void Sleep();
    std::string ToString() const;
    void Print(std::string message);
};

int main() {
  const int size = 8;
  DiningTable table(size);
  return 0;
}

DiningTable::DiningTable(int size) {
  for (int index = 0; index < size; ++index) {
    chopsticks.emplace_back();
  }
  std::deque<Philosopher> philosophers;
  for (int index = 0; index < size; ++index) {
    philosophers.emplace_back(index, *this, chopsticks[index], chopsticks[(index + 1) % size]);
  }
  ready = true;
  std::this_thread::sleep_for(std::chrono::seconds(120));
  ready = false;
}

Philosopher::Philosopher(int index, const DiningTable& table, Chopstick& left, Chopstick& right)
  : index_(index), dining_table_(table), left_(left), right_(right), thread_(&Philosopher::Dine, this) { }

void Philosopher::Dine() {
  do {
    if (std::uniform_int_distribution(0, 1)(generator_)) {
      Eat();
    } else {
      Talk();
    }
  } while (dining_table_.ready);
}

Philosopher::~Philosopher() {
  thread_.join();
}

void Philosopher::Sleep() {
  std::this_thread::sleep_for(std::chrono::milliseconds(std::uniform_int_distribution(1'000, 5'000)(generator_)));
}

std::string Philosopher::ToString() const {
  return "Philosopher " + std::to_string(index_);
}

void Philosopher::Print(std::string message) {
  std::scoped_lock guard(cout_mutex);
  std::cout << ToString() << " " << message << "\n";
}

void Philosopher::Eat() {
  Print("is waiting for chopsticks");
  std::scoped_lock guard(left_.mutex, right_.mutex);
  Print("is eating");
  Sleep();
  Print("has finished eating");
}

void Philosopher::Talk() {
  Print("is talking");
  Sleep();
  Print("has finished talking");
}
