"""The unchanged insert fit coupon, named for the R8 package."""
import argparse
from make_retro_r7_probe import export

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('root');args=ap.parse_args()
    export(args.root,'R8')
