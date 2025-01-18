from ipsurv.core.object_factory import ObjectFactory

from ipsurv.ip_surv_cmd import IpSurvCmd

'''
Show original headers message.

Specification:
- Customizing LineSerializer class.
- Creating ObjectFactory class.

Command:
# python3 object_factory_original_headers.py
'''

from ipsurv.serializer.line_serializer import LineSerializer


class MySerializer(LineSerializer):
    def output_begin(self, mode, args, rows):
        super().output_begin(mode, args, rows)

        message = r'''
 __  .______     _______. __    __  .______     ____    ____
|  | |   _  \   /       ||  |  |  | |   _  \    \   \  /   /
|  | |  |_)  | |   (----`|  |  |  | |  |_)  |    \   \/   /
|  | |   ___/   \   \    |  |  |  | |      /      \      /
|  | |  |   .----)   |   |  `--'  | |  |\  \----.  \    /
|__| | _|   |_______/     \______/  | _| `._____|   \__/

'''

        print('\033[34m' + message + '\033[0m')

    def output_complete(self, mode, args, rows):
        print('')
        print('\033[34m' + 'Complete!' + '\033[0m')


class MyObjectFactory(ObjectFactory):
    def create_serializer(self, args):
        serializer = MySerializer(args)

        return serializer


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
