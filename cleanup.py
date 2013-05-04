import redis
import os


def main():
    illness_dir = os.path.join(os.path.dirname(__file__), 'illness_docs')
    for json_file in os.listdir(illness_dir):
        file_path = os.path.join(illness_dir, json_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.flushall()

if __name__ == '__main__':
    main()
