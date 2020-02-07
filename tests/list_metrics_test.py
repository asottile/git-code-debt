from git_code_debt.list_metrics import color
from git_code_debt.list_metrics import CYAN
from git_code_debt.list_metrics import main
from git_code_debt.list_metrics import NORMAL


def test_list_metrics_smoke(capsys):
    # This test is just to make sure that it doesn't fail catastrophically
    main([])
    assert capsys.readouterr().out


def test_list_metrics_no_color_smoke(capsys):
    main(['--color', 'never'])
    out, err = capsys.readouterr()
    assert '\033' not in out
    assert '\033' not in err


def test_color_no_color():
    ret = color('foo', 'bar', False)
    assert ret == 'foo'


def test_colored():
    ret = color('foo', CYAN, True)
    assert ret == CYAN + 'foo' + NORMAL
