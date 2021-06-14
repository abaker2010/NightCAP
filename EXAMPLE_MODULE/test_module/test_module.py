# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from nightcapclient import NightcapClient
from nightcapcore import *
import os
#endregion

class SomePackageName(NightcapClient):
    def __init__(self):
        # super(NightcapScanner, self).__init__()
        NightcapClient.__init__(self)
        # self.simple_report = NightcapSimpleReport(__file__, self.basedata['0'])
        self.found_count = 0


    def onProcess(self, pkt):
        self.found_count += 1

    def onClose(self):
        self.printer.print_formatted_check("Total packets")
        self.printer.print_formatted_additional("Count", str(self.found_count), leadingTab=3)

    def onReport(self):
        # print("Generating Reports")
        pass

    def onConsolePrint(self):
        pass


def main():
    ncore = SomePackageName()
    try:
        
        # ncore.printer.print_underlined_header("Protocol Overview")
        ncore.run()

    # ncore.simple_report.name = "Test Report"
    # custom_style = str(os.path.dirname(__file__)) + '/src/style.css'
    # ncore.simple_report.add_custom_style_sheet(custom_style)
    # ncore.simple_report.replace_original_style_sheet = True
    # print("Using custom style sheet", custom_style)

    # header_key = ncore.simple_report.add_header(NightcapSimpleReportHeader("IPs"))
    # header_key1 = ncore.simple_report.add_header(NightcapSimpleReportHeader("header two"))

    # region Analyzing PCAP
    # print("Looking into file")
    # total_counted = 0
    # for packet in ncore.pcapFiles:
    #     # print(packet)
    #     for pkt in packet:
    #         print(dir(pkt))
    # for packet in ncore.pcapFiles:
    #     print("\n", packet.input_filename)
    #     count_of_lines_in_pcap = 0
    #     ncore.simple_report.add_header_data(header_key, NightcapSimpleReportParagraph(packet.input_filename))
    #     # for pkt in packet:
    #     #     count_of_lines_in_pcap += 1
    #     #     sys.stdout.write("\r\t  [?] "  + "Packet Num : "  + str(count_of_lines_in_pcap))
    #     # total_counted += count_of_lines_in_pcap

    # print("\n\n")
    # print("processed pcap in developer package (line count)", total_counted)

    # endregion

    # ncore.simple_report.print_report()

    # ncore.simple_report.save()
    except Exception as e:
        ncore.printer.print_error(e)
        print(e)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)
    finally:
        exit()
