import requests

def main():

    com = input()
    col = int(input())
    g = 1
    if int(com[com.find('|')-1])==0:

        while int(com[com.find('|')-g]) == 0:
            g=g+1
        ind = int(com[(com.find('|')-g-2) : (com.find('|'))])

    else:
        ind = int( com[(com.find('|')-g-2) : (com.find('|'))] )

    i=1

    while i <= col:
        prt = com[ : (com.find('|')-g-2) ]+ str(ind+i)+com[ com.find('|') : ]
        print(prt)
        i=i+1

if __name__ == "__main__":
    main()