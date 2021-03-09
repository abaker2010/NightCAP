# # Copyright 2020 by Aaron Baker.
# # All rights reserved.
# # This file is part of the Nightcap Project,
# # and is released under the "MIT License Agreement". Please see the LICENSE
# # file that should have been included as part of this package.
# # from nightcapcore import NightcapSimpleReport, NightcapCore
# from nightcapcore import *
# import os
# # from nightcapcore.report.widgets.header import NightcapSimpleReportHeader

# class SomePackageName(NightcapCore):
#     def __init__(self):
#         NightcapCore.__init__(self)
#         self.simple_report = NightcapSimpleReport(__file__, self.basedata['0'])

# def main():
#     print("\n", "\t[-] Able to run from module")
#     ncore = SomePackageName()

#     ncore.simple_report.name = "Test Report"
#     custom_style = str(os.path.dirname(__file__)) + '/src/style.css'
#     # ncore.simple_report.add_custom_style_sheet(custom_style)
#     # ncore.simple_report.replace_original_style_sheet = True
#     print("Using custom style sheet", custom_style)

#     header_key = ncore.simple_report.add_header(NightcapSimpleReportHeader("IPs"))
#     # header_key1 = ncore.simple_report.add_header(NightcapSimpleReportHeader("header two"))
    
#     #region Analyzing PCAP
#     print("Looking into file")
#     total_counted = 0
#     for packet in ncore.pcapFiles:
#         # print(packet)
#         for pkt in packet:
#             print(dir(pkt))
#     # for packet in ncore.pcapFiles:
#     #     print("\n", packet.input_filename)
#     #     count_of_lines_in_pcap = 0
#     #     ncore.simple_report.add_header_data(header_key, NightcapSimpleReportParagraph(packet.input_filename))
#     #     # for pkt in packet:
#     #     #     count_of_lines_in_pcap += 1
#     #     #     sys.stdout.write("\r\t  [?] "  + "Packet Num : "  + str(count_of_lines_in_pcap))
#     #     # total_counted += count_of_lines_in_pcap

#     print("\n\n")
#     print("processed pcap in developer package (line count)", total_counted)

#     #endregion

#     ncore.simple_report.print_report()

#     ncore.simple_report.save()

        
# if __name__ == '__main__':
#     try:
#         main()
#     except KeyboardInterrupt:
#         exit()
#     except Exception as e:
#         print(e)
#     finally:        
#         exit()