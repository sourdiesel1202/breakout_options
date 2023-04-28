print(__name__)
import importlib

from pathlib import Path

strategies = Path('strategy_files').glob('*.py')
inventory = []
for strategy in strategies:
    stem = strategy.stem
    stem_fn = importlib.import_module(f'strategy_files.{stem}', stem)
    inventory.append((stem, stem_fn.strategy_name))

if __name__ == '__main__':
    ...
