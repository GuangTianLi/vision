import json
import logging
import os
import socketserver
import threading
import zipfile

from vision.creator import CreatorRunner

logger = logging.getLogger(__name__)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    settings = None
    creator = None
    def make_archive(self, source_paths, archive_path, root_path):
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for f in source_paths:
                logger.info("archiving file {}".format(f))
                zip_file.write(f, os.path.relpath(f, root_path))
            logger.info("create file {}".format(archive_path))

    def handle(self):
        creator = ThreadedTCPRequestHandler.creator
        data_loaded = json.loads(self.request.recv(2048).decode('utf-8'))  # data loaded
        logger.info("receive data: {}".format(data_loaded))
        data_report_name = data_loaded.get('data_report_name', None)
        file_name = data_loaded.get('file_name', None)
        data_report_root_path = data_loaded.get('data_report_add', None)
        dont_archive = data_loaded.get('dont_archive', False)
        data_report_file_add = data_report_root_path + file_name.replace('.txt', '.zip')
        try:
            if data_report_name:
                creator.file_name = file_name
                creator.create(data_report_name)
                if ThreadedTCPRequestHandler.settings.get("SVG_FILE"):
                    file_list = list(creator.file_dict.keys()) + list(creator.file_dict.values())
                else:
                    file_list = list(creator.file_dict.keys())
                if dont_archive:
                    data_report_file_add = file_list
                else:
                    self.make_archive(file_list, data_report_file_add, data_report_root_path)
                response = {'result': data_report_file_add}
                logger.info('send data: {}'.format(response))
                self.request.sendall(json.dumps(response).encode('utf-8'))
        except Exception as e:
            logger.error(e)
            response = {'result': -1}
            self.request.sendall(json.dumps(response).encode('utf-8'))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Server(object):
    def __init__(self, settings=None):
        self.settings = settings
        ThreadedTCPRequestHandler.settings = self.settings
        ThreadedTCPRequestHandler.creator = CreatorRunner(ThreadedTCPRequestHandler.settings)

    def start(self, *args, **kwargs):
        '''
        This method is to run DataReport server
        '''
        HOST, PORT = self.settings.get("SERVER_HOST", "127.0.0.1"), self.settings.get("SERVER_PORT")

        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        server.serve_forever()
