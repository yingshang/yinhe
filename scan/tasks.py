from celery import task,platforms
import nmap
platforms.C_FORCE_ROOT = True 
@task()
def scan(host,port):
    nm = nmap.PortScanner()
    nm.scan(host,port)
    data = nm.csv()
    print data
    return data

