from celery import task
import nmap
@task()
def scan(host,port):
    nm = nmap.PortScanner()
    nm.scan(host,port)
    data = nm.csv()
    return data