from discnerd.cli import cli
from click.testing import CliRunner
import os
# def test_load_config():
#     print("Test load config")
#     discnerd.cli.load_config(f"{discnerd.cli.DEFAULT_CONFIG_PATH}/{discnerd.cli.DEFAULT_CONFIG_NAME}")

def test_add_set():
    runner = CliRunner()
    result = runner.invoke(cli, ['--config','tests/testconfig', 'add-set', '--name', 'test-set'])
    print(result.output)
    assert result.exit_code == 0
    os.remove('testdata.yml')

    
def test_add_disc():
    runner = CliRunner()
    result = runner.invoke(cli, ['--config','tests/testconfig', 'add-set', '--name', 'test-set'])
    assert result.exit_code == 0
    result = runner.invoke(cli, ['--config','tests/testconfig',
         'add',
         '--set', 'test-set',
         '--name', 'testdisc',
         '--speed', '7',
         '--glide', '4',
         '--fade', '2',
         '--turn', '1.0',
        '--brand', 'testbrand',
    
    ])
    print(result.output)
    assert result.exit_code == 0
    os.remove('testdata.yml')
