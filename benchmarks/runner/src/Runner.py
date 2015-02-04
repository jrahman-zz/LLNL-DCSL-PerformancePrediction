
import argparse



def parse_args():

    parser = argparse.ArgumentParser(description='Runner')
    parser.add_argument()

def main():

    feature_map = {}

    # Example
    memory_stream_1k = MemoryStream1K()
    memory_stream_1m = MemoryStream1M()
    memory_stream_1g = MemoryStream1G()

    feature_map['memory_stream_1k'] = memory_stream_1k
    feature_map['memory_stream_1m'] = memory_stream_1m
    feature_map['memory_stream_1g'] = memory_stream_1g


if __name__=="__ma

    
