from discnerd.cli import cli
from discnerd.data import *
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
    
def test_remove_disc():
    runner = CliRunner()
    result = runner.invoke(cli, ['--config','tests/testconfig', 'add-set', '--name', 'test-set'])
    assert result.exit_code == 0
    myDiscs = MyDiscs()
    myDiscs.load("testdata.yml")
    test_set = myDiscs.get_set('test-set')

    assert test_set.number_of_discs() == 0
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
    result = runner.invoke(cli, ['--config','tests/testconfig',
         'remove',
         '--set', 'test-set',
         '--myid', '1',
        ])
    print(result.output)
    assert result.exit_code == 0

    myDiscs = MyDiscs()
    myDiscs.load("testdata.yml")
    test_set = myDiscs.get_set('test-set')
    print(test_set)
    assert test_set.number_of_discs() == 0
    
    os.remove('testdata.yml')
