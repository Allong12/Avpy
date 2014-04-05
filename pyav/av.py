from ctypes import CDLL, RTLD_GLOBAL, util

def version():
    
    '''
    Return libavcodec version as a tuple: major, minor, patch version
    '''
    
    libavcodec = util.find_library('avcodec')
    version = CDLL(libavcodec, mode=RTLD_GLOBAL).avcodec_version() 
    
    return version >> 16 & 0xFF, version >> 8 & 0xFF, version & 0xFF

def findModuleName():
   
    '''
    find libav python binding to import

    on error, raise an ImportError exception
    '''

    versionDict = { 
            52: { 
                # libav 0.5.9
                # ffmpeg 0.5.10 ~ libav 0.5.9
                (20, 40): 'av5', 
                # libav 0.6.6
                # ffmpeg 0.6.6 ~ libav 0.6.6
                (70, 75): 'av6',
                },
            53: {
                (0, 10): 'av7',
                (30, 40): 'av8',
                }
            }

    major, minor, micro = version()	

    if major in versionDict:
        
        intv = versionDict[major]
        libName = None
        
        for k in intv.keys():
            if minor >= k[0] and minor < k[1]:
                libName = intv[k]
                break

        if libName is None:
            raise ImportError('ffmpeg/libav minor version not supported')
    else:
        raise ImportError('ffmpeg/libav major version not supported')

    return libName

_moduleName = findModuleName() 
# import module
_temp = __import__('pyav.version', globals(), locals(), [_moduleName])
# import as lib
lib = getattr(_temp, _moduleName)

