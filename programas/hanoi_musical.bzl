Hanoi |:
    Mueve 5 1 2 3
:|

Mueve n ori dst aux |:
    if n > 0 |:
        Mueve (n - 1) ori aux dst
        (:) C + n
        Mueve (n - 1) aux dst ori
    :|
:|