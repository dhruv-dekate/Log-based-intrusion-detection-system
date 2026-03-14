import re
from datetime import datetime
import pandas as pd


LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<time>.*?)\] "(?P<method>\S+)? (?P<endpoint>\S+)? .*?" (?P<status>\d{3}) (?P<size>\d+) ".*?" "(?P<agent>.*?)"'
)

def parse_log(path):
    row = []
    with open(path, 'r') as f:
        for line in f:
            match = LOG_PATTERN.match(line)
            if match:
                data = match.groupdict()
                data['time'] = datetime.strptime(data['time'], '%d/%b/%Y:%H:%M:%S %z')
                row.append(data)

    df  = pd.DataFrame(row)
    df['status'] = df['status'].astype(int)
    df['size'] = df['size'].astype(int)
    return df[['ip', 'time', 'method', 'endpoint', 'status', 'size', 'agent']]
"""
if __name__ == "__main__":
    df = parse_log('data/access.log')
    print(df.head(3))
    print(df.info())
    total_lines = len(df)
    print(f'Total lines: {total_lines}')

"""