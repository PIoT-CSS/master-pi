from mqtt.publish import Publisher

'''
Main
'''

def main():
    pub = Publisher()
    pub.publish('test', 1)


if __name__ == '__main__':
        main()
