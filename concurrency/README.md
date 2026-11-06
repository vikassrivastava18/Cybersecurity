## Concurrency
Concurrency means multiple computations are happening at the same time. Concurrency is everywhere in modern programming, whether we like or not:
- Multiple computers in a network
- Multiple applications running on a computer
- Multiple processors in a computer

Example: A single account, with a dollar balance stored in the balance variable, and two operations deposit and withdraw that simply add or remove a dollar.

```
// suppose all the cash machines share a single bank account
private static int balance = 0;

private static void deposit() {
    balance = balance + 1;
}
private static void withdraw() {
    balance = balance - 1;
}
```

Below code if run multiple times a day may not result in expected 0 balance for the user

```
// each ATM does a bunch of transactions that
// modify balance, but leave it unchanged afterward
private static void cashMachine() {
    for (int i = 0; i < TRANSACTIONS_PER_MACHINE; ++i) {
        deposit(); // put a dollar in
        withdraw(); // take it back out
    }
}
```

### Interleaving

if the events happen in seauence, nothing breaks:

```
A get balance (balance=0)
A add 1        
A write back the result (balance=1)
                                    B get balance (balance=1)
                                    B add 1     
                                    B write back the result (balance=2)
```

In case of interleaving that happen simultaneously, this could cause a proble.

```
A get balance (balance=0)
                                    B get balance (balance=0)
A add 1         
                                    B add 1     
A write back the result (balance=1)
                                    B write back the result (balance=1)
```

The above is an example of a race condition.


### Remedy
Using Transactions

```
import sqlite3
import threading
import time

def withdraw(amount):

    conn = sqlite3.connect(
        "bank.db",
        timeout=10
    )

    cursor = conn.cursor()

    try:
        # Acquire write transaction immediately
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute(
            "SELECT balance FROM accounts WHERE id = 1"
        )

        balance = cursor.fetchone()[0]

        if balance >= amount:

            time.sleep(0.5)

            new_balance = balance - amount

            cursor.execute(
                "UPDATE accounts SET balance = ? WHERE id = 1",
                (new_balance,)
            )

            conn.commit()

            print(f"Withdrawal successful: {amount}")

        else:
            conn.rollback()
            print("Insufficient balance")

    except sqlite3.Error as e:
        conn.rollback()
        print("Database error:", e)

    finally:
        conn.close()


t1 = threading.Thread(target=withdraw, args=(800,))
t2 = threading.Thread(target=withdraw, args=(800,))

t1.start()
t2.start()

t1.join()
t2.join()
```

Using threading.Lock() in Python

```
import threading
import time

balance = 1000

lock = threading.Lock()

def withdraw(amount):
    global balance

    with lock:
        if balance >= amount:
            time.sleep(0.1)
            balance -= amount
            print(f"Withdrawal successful: {amount}")
        else:
            print("Insufficient balance")

t1 = threading.Thread(target=withdraw, args=(800,))
t2 = threading.Thread(target=withdraw, args=(800,))

t1.start()
t2.start()

t1.join()
t2.join()

print("Final balance:", balance)
```