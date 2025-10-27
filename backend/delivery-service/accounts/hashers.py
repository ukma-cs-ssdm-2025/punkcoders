from django.contrib.auth.hashers import Argon2PasswordHasher


class MyArgon2PasswordHasher(Argon2PasswordHasher):
    """
    A custom Argon2 password hasher with increased effort values for better
    security, based on OWASP recommendations.

    - time_cost: The number of passes over the memory.
    - memory_cost: The amount of memory to use in KiB.
    - parallelism: The number of parallel threads to use.
    """

    time_cost = 3
    memory_cost = 12288
    parallelism = 1
