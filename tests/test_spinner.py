"""Testes de Spinner.set_message, sem depender de captura de terminal."""
import time

from src.cli.spinner import Spinner


def test_set_message_updates_displayed_text():
    spinner = Spinner("mensagem inicial")
    assert spinner._message == "mensagem inicial"

    spinner.set_message("mensagem atualizada")
    assert spinner._message == "mensagem atualizada"


def test_set_message_works_while_spinning(capsys):
    with Spinner("inicio") as spinner:
        time.sleep(0.15)
        spinner.set_message("meio")
        time.sleep(0.15)
        spinner.set_message("fim")
        time.sleep(0.15)

    out = capsys.readouterr().out
    assert "inicio" in out
    assert "meio" in out
    assert "fim" in out


def test_exit_clears_the_longest_message_shown():
    with Spinner("curta") as spinner:
        spinner.set_message("uma mensagem bem mais longa que a inicial")

    assert spinner._max_len == len("uma mensagem bem mais longa que a inicial")
