import java.util.concurrent.Semaphore;
import java.util.Random;

class Chopstick {
    public Semaphore mutex = new Semaphore(1);

    public boolean take() {
        return mutex.tryAcquire();
    }

    public void release() {
        mutex.release();
    }
}

class Philosopher extends Thread {
    private Chopstick lowChopstick;
    private Chopstick highChopstick;
    private String name;
    private static Random random = new Random();

    public Philosopher(String name, Chopstick lowChopstick, Chopstick highChopstick) {
        this.name = name;
        this.lowChopstick = lowChopstick;
        this.highChopstick = highChopstick;
    }

    public void eat() {
        if (lowChopstick.take()) {
            if (highChopstick.take()) {
                Log.msg(name + " is eating");
                Log.Delay(random.nextInt(5000));
                lowChopstick.release();
                highChopstick.release();
            } else {
                lowChopstick.release();
                Log.msg(name + " is waiting");
                Log.Delay(random.nextInt(5000));
            }
        } else {
            Log.msg(name + " is waiting");
            Log.Delay(random.nextInt(5000));
        }
    }

    public void think() {
        Log.msg(name + " is thinking");
        Log.Delay(random.nextInt(5000));
    }

    @Override
    public void run() {
        try {
            sleep(2000);
        } catch (InterruptedException ex) {
            Log.msg("Interruption happend while waiting");
        }

        while (true) {
            eat();
            think();
        }
    }

}

class Log {
//  public static Semaphore mutex = new Semaphore(1);

    public static void msg(String msg) {
//      do {
//      } while (!mutex.tryAcquire());
        System.out.println(msg);
//      mutex.release();
    }

    public static void Delay(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException ex) {
            Log.msg("Interruption happend while waiting");
        }
    }
}

public class Dine {
    public static void main(String[] args) {
        Chopstick[] chopsticks = new Chopstick[8];
        for (int chopstick_id = 0; chopstick_id < chopsticks.length; chopstick_id++) {
            chopsticks[chopstick_id] = new Chopstick();
        }

        String[] names = { "Aristotle", "Bacon", "Confucius", "Descartes", "Eratosthenes", "al-Farabi", "Gödel",
                "Heraclitus" };
        Philosopher[] philosophers = new Philosopher[8];
        for (int philosopher_id = 0; philosopher_id < philosophers.length; philosopher_id++) {
            if (philosopher_id != philosophers.length - 1) {
                philosophers[philosopher_id] = new Philosopher(names[philosopher_id], chopsticks[philosopher_id],
                        chopsticks[philosopher_id + 1]);
                philosophers[philosopher_id].start();
            } else {
                philosophers[philosopher_id] = new Philosopher(names[philosopher_id], chopsticks[0],
                        chopsticks[philosopher_id]);
                philosophers[philosopher_id].start();
            }
        }
    }
}
