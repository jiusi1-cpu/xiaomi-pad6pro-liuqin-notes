import sys,pathlib,struct,hashlib,json,gzip
sys.path.insert(0,str(pathlib.Path('work/deps').resolve()))
import lz4.block

def unpack(path):
    b=pathlib.Path(path).read_bytes()
    assert b[:8]==b'ANDROID!' and struct.unpack_from('<I',b,40)[0]==4
    k,r=struct.unpack_from('<II',b,8)
    offset=4096+((k+4095)//4096)*4096
    compressed=b[offset:offset+r]
    if compressed[:4]==bytes.fromhex('02214c18'):
        pos=4; chunks=[]
        while pos<len(compressed):
            length=struct.unpack_from('<I',compressed,pos)[0]; pos+=4
            if not length: break
            chunk=compressed[pos:pos+length]; assert len(chunk)==length
            chunks.append(lz4.block.decompress(chunk,uncompressed_size=8*1024*1024)); pos+=length
        data=b''.join(chunks)
    elif compressed[:2]==b'\x1f\x8b': data=gzip.decompress(compressed)
    else: raise RuntimeError('Unsupported ramdisk compression')
    entries={}; pos=0
    while pos<len(data):
        hdr=data[pos:pos+110]; assert hdr[:6] in (b'070701',b'070702')
        fields=[int(hdr[6+i*8:14+i*8],16) for i in range(13)]
        size,nlen=fields[6],fields[11]
        name=data[pos+110:pos+110+nlen-1].decode()
        begin=(pos+110+nlen+3)//4*4
        content=data[begin:begin+size]; assert len(content)==size
        pos=(begin+size+3)//4*4
        if name=='TRAILER!!!': break
        entries[name]=(fields[1],content)
    return b,b[4096:4096+k],entries

stock,kernel,a=unpack('outputs/boot-stock-OS3.0.7.0.VMYCNXM.img')
patched,newkernel,b=unpack('outputs/boot-KernelSU-v3.3.1-OS3.0.7.0.VMYCNXM.img')
assert kernel==newkernel,'Kernel changed unexpectedly'
assert stock[16:44]==patched[16:44],'Boot metadata changed unexpectedly'
assert b['init.real']==a['init'],'Original init not preserved'
assert b['init'][1]==pathlib.Path('work/ksuinit-aarch64').read_bytes(),'Wrong ksuinit'
assert b['kernelsu.ko'][1]==pathlib.Path('work/lkm-aarch64-android12-5.10_kernelsu.ko').read_bytes(),'Wrong LKM'
for name,value in a.items():
    if name!='init': assert b[name]==value,f'Unexpected modification to {name}'
assert set(b)-set(a)=={'init.real','kernelsu.ko'},'Unexpected extra files'
assert len(patched)==len(stock)==201326592
report={
    'stock_boot_sha256':hashlib.sha256(stock).hexdigest(),
    'patched_boot_sha256':hashlib.sha256(patched).hexdigest(),
    'kernel_sha256_unchanged':hashlib.sha256(kernel).hexdigest(),
    'stock_init_preserved':True,
    'all_other_stock_ramdisk_entries_preserved':True,
    'official_v3_3_1_lkm_and_init_verified':True,
    'boot_metadata_preserved':True,
    'device_boot_tested':False,
    'root_verified_on_device':False,
}
pathlib.Path('work/boot-verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
