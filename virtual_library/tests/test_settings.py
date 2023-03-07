import os
import environ
import pytest



def test_secret_key_not_in_env():
    with open('.env.example', 'w') as f:
        f.write('')

    os.environ.pop('SECRET_KEY_TEST', None)
    with pytest.raises(Exception) as excinfo:
        env = environ.Env()
        SECRET_KEY = env('SECRET_KEY')
        assert str(excinfo.value) == 'Set the SECRET_KEY environment variable'

def test_secret_key_in_env():
    with open('.env.example', 'w') as f:
        f.write('SECRET_KEY=test_secret_key\n')

    os.environ['SECRET_KEY'] = 'test_secret_key'
    env = environ.Env()
    SECRET_KEY = env('SECRET_KEY')
    assert SECRET_KEY == 'test_secret_key'
