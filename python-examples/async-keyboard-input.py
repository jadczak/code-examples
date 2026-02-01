import asyncio
import msvcrt

from dataclasses import dataclass


@dataclass(slots=True)
class Keys():
    """
    Slots is set to True so the dataclass takes less space.

    This keymapping assumes that you are using getwch, othewise
    there will be different escape keys.

    There are only lower case letters in this mapping.
    """
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"
    SPECIAL1 = b'\xc3\xa0'.decode()
    SPECIAL2 = b'\x00'.decode()
    LEFT = SPECIAL1 + "K"
    DOWN = SPECIAL1 + "P"
    RIGHT = SPECIAL1 + "M"
    UP = SPECIAL1 + "H"
    INSERT = SPECIAL1 + "R"
    HOME = SPECIAL1 + "G"
    DEL = SPECIAL1 + "S"
    END = SPECIAL1 + "O"
    PG_UP = SPECIAL1 + "I"
    PG_DOWN = SPECIAL1 + "Q"
    F1 = SPECIAL2 + ";"
    F2 = SPECIAL2 + "<"
    F3 = SPECIAL2 + "="
    F4 = SPECIAL2 + ">"
    F5 = SPECIAL2 + "?"
    F6 = SPECIAL2 + "@"
    F7 = SPECIAL2 + "A"
    F8 = SPECIAL2 + "B"
    F9 = SPECIAL2 + "C"
    F10 = SPECIAL2 + "D"
    # F11 doesn't get captured.
    F12 = SPECIAL1 + b"\xc2\x86".decode()


async def get_key(queue: asyncio.Queue):
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key == Keys.SPECIAL1 or key == Keys.SPECIAL2:
                key += msvcrt.getwch()
                await queue.put(key)
            else:
                await queue.put(key.lower())  # so we aren't case sensitive.
        else:
            await asyncio.sleep(0.001)


async def main():
    queue = asyncio.Queue()
    keyboard_task = asyncio.create_task(get_key(queue))
    key = ""
    while (key != Keys.Q):
        if not queue.empty():
            key = await queue.get()
            # do something with the key that is captured.
        await asyncio.sleep(0.001)
    keyboard_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
