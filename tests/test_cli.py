from click.testing import CliRunner
from cli.main import cli

def test_cli_base_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Red Dead Redemption 2 Gambling Utility" in result.output

def test_cli_blackjack_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["blackjack", "--help"])
    assert result.exit_code == 0
    assert "Blackjack utility commands" in result.output

def test_cli_poker_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["poker", "--help"])
    assert result.exit_code == 0
    assert "Poker utility commands" in result.output

def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "rdr2-gambler, version 0.1.0" in result.output
