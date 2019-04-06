from .models import *
import datetime

def main():
    """
    This script is to generate the ticket number for each day. This has to be schedule fo reach day
    """
    try:
        tday = datetime.date.today()
        if not TicketDetail.objects.filter(date_of_journey = tday).exists():
            ticket_list = []
            for ticket_seq in range(1,38):
                if ticket_seq in [7,8,15,16,23,24,31,32]:
                    ticket_list.append('RAC' + str(tday).replace('-','') + '000' + str(ticket_seq))
                elif ticket_seq in range(1,33):
                    ticket_list.append('CNF' + str(tday).replace('-','') + '000' + str(ticket_seq))
                else:
                    ticket_list.append('WL' + str(tday).replace('-','') + '000' + str(ticket_seq))
            
            
            upper = BerthType.objects.get(berth_type = "UPPER")
            middle = BerthType.objects.get(berth_type = "MIDDLE")
            lower = BerthType.objects.get(berth_type = "LOWER")
            side = BerthType.objects.get(berth_type = "SIDE")
            
            available = TicketStatus.objects.get(status_code = 'AVL' )
            confirm = TicketStatus.objects.get(status_code = 'CNF' )
            
            S1 = Coach.objects.get(coach_nbr='S1')
            S2 = Coach.objects.get(coach_nbr='S2')
            S3 = Coach.objects.get(coach_nbr='S3')
            S4 = Coach.objects.get(coach_nbr='S4')
            
            
            for seq, ticket_nbr in enumerate(ticket_list):
                sheet_nbr = seq + 1
                if sheet_nbr in [3,6,11,14,19,22,27,30]:
                    berth_type_id = upper
                elif sheet_nbr in [2,5,10,13,18,21,26,29]:
                    berth_type_id = middle
                elif sheet_nbr in [1,4,9,12,17,20,25,28]:
                    berth_type_id = lower
                elif sheet_nbr in [7,8,15,16,23,24,31,32]:
                    berth_type_id = side
                else:
                    berth_type_id = None
            
                if ticket_nbr.startswith('CNF'):
                    status_id = available
                else:
                    status_id = None
            
                if seq in range(0,8):
                    coach_id = S1
                elif seq in range(8,16):
                    coach_id = S2
                elif seq in range(16,24):
                    coach_id = S3
                elif seq in range(24,32):
                    coach_id = S4
                else:
                    coach_id = None
                    
                    
                ticket_obj = TicketDetail(ticket_nbr = ticket_nbr, 
                                          berth_type_id = berth_type_id,
                                          status_id = status_id, 
                                          coach_id = coach_id,
                                          date_of_journey = tday)
                ticket_obj.save()
        else:
            print("Tickets are already generated for " + str(tday))
        
    except Exception as e:
        print(e)   
         
if __name__ == '__main__':
    main()