import requests

def main():

    com = input()
    col = int(input())
    g = 1

    ind = int(com[(com.find('|') - 4) : (com.find('|'))])
    print(ind)
    i=1

    while i <= col:
        prt = com[ : (com.find('|')-4) ]+ str(ind+i)+com[ com.find('|') : ]
        print(prt)
        i=i+1

if __name__ == "__main__":
    main()
