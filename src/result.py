from typing import Generic, TypeVar, Union, Optional

T = TypeVar("T")
E = TypeVar("E")


class _Ok(Generic[T]):
    """
    Representa um resultado bem-sucedido, armazenando um valor opcional do tipo T.

    Uso:
        resultado = Ok(123)
        if resultado.is_ok:
            print(resultado.value)  # Saída: 123
    """

    def __init__(self, value: Optional[T] = None) -> None:
        self.value = value
        self.is_ok = True


class _Err(Generic[E]):
    """
    Representa um resultado de erro, armazenando um valor de erro do tipo E.

    Uso:
        erro = Err("Falha na operação")
        if not erro.is_ok:
            print(erro.value)  # Saída: Falha na operação
    """

    def __init__(self, value: E) -> None:
        self.value = value
        self.is_ok = False


Result = Union[_Ok[T], _Err[E]]


def Ok(value: Optional[T] = None) -> _Ok[T]:
    """
    Função para criar um resultado bem-sucedido do tipo _Ok[T].

    Uso:
        resultado = Ok(123)
    """
    return _Ok(value)


def Err(value: E) -> _Err[E]:
    """
    Função para criar um resultado de erro do tipo _Err[E].

    Uso:
        erro = Err("Falha na operação")
    """
    return _Err(value)
