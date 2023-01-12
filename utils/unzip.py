import gzip, hashlib

def check_sum(file: str):
    with open(file, 'rb') as f:
        bytes = f.read()
        hash = hashlib.sha256(bytes)
        return hash.hexdigest()

def unzip_gz(gz_file: str):
    with gzip.open(gz_file, 'rb') as f_in, open(gz_file.replace('.gz', ''), 'wb') as f_out:
        f_out.write(f_in.read())

if __name__ == '__main__':
    f = 'D:\ChromeDownload\openwrt-21.02.2-rockchip-armv8-friendlyarm_nanopi-r2s-ext4-sysupgrade.img.gz'
    print(check_sum(f))
    unzip_gz(f)
