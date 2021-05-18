This example looks at what happens when multiple clients attempt to increment a counter simultaneously.

This test isn't meant as shade on SQLite -- which explicitly states in its documentation that it isn't designed for this level of concurrency. It does serve as a good reminder to understand what sorts of guarantees your database offers, though!