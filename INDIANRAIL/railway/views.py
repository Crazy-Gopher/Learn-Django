from django.shortcuts import render, render_to_response
from .models import *
#from django.views.decorators.csrf import csrf_exempt
import psycopg2
import datetime
from django.http import JsonResponse, Http404

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    #num_tickets=TicketDetail.objects.all().count()
    #'num_books':num_tickets,

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'index.html', context={ 'num_visits':num_visits})


def cancel_ticket(request):
    return render(request, 'railway/cancel_ticket_form.html', context={ })


def cancel(request):
    response_data = {}
    try:
        if request.method == 'POST':
            ticket_nbr = request.POST['ticket_nbr']
            if not ticket_nbr:
                raise Http404("URL doesn't exists")
            
            try:
                to_be_cancelled_ticket_obj = TicketDetail.objects.get(ticket_nbr=ticket_nbr)
            except Exception as e:
                raise Http404("Ticket number doesn't exists")
            cancel_status_id = TicketStatus.objects.get(status_code='CAN')
            if to_be_cancelled_ticket_obj.status_id.status_code == 'CNF':
                coach_list = Coach.objects.all().order_by("coach_nbr")
                for coach in coach_list:
                    rac_ticket_obj = TicketDetail.objects.filter(coach_id=coach, status_id__status_code = 'RAC').first()
                    if rac_ticket_obj:
                        break
                    
                for coach in coach_list:
                    wl_ticket_obj = TicketDetail.objects.filter(coach_id=coach, status_id__status_code = 'WL').first()
                    if wl_ticket_obj:
                        break

                if wl_ticket_obj:
                    wl_ticket_obj.status_id = rac_ticket_obj.status_id 
                    wl_ticket_obj.coach_id = rac_ticket_obj.coach_id 
                    wl_ticket_obj.berth_type_id = rac_ticket_obj.berth_type_id
                    wl_ticket_obj.save()
                
                if rac_ticket_obj:
                    rac_ticket_obj.status_id = to_be_cancelled_ticket_obj.status_id 
                    rac_ticket_obj.coach_id = to_be_cancelled_ticket_obj.coach_id
                    rac_ticket_obj.berth_type_id = to_be_cancelled_ticket_obj.berth_type_id
                    rac_ticket_obj.save()
                
            elif to_be_cancelled_ticket_obj.status_id.status_code == 'RAC':
                for coach in coach_list:
                    wl_ticket_obj = TicketDetail.objects.filter(coach_id=coach, staus_id__status_code = 'WL').first()
                    if wl_ticket_obj:
                        break

                if wl_ticket_obj:
                    wl_ticket_obj.status_id = rac_ticket_obj.status_id 
                    wl_ticket_obj.coach_id = rac_ticket_obj.coach_id 
                    wl_ticket_obj.berth_type_id = rac_ticket_obj.berth_type_id
                    wl_ticket_obj.save()

            to_be_cancelled_ticket_obj.status_id = cancel_status_id
            to_be_cancelled_ticket_obj.save()
            response_data['ticket_nbr'] = ticket_nbr
    except Exception as e:
        print(e)
    return JsonResponse(response_data)


def book_ticket(request):
    return render(request, 'railway/book_ticket_form.html', context={ })


def book(request):
    passenger_detail = {}
    response_data = {}
    if request.method == 'POST':
        passenger_detail['full_name'] = request.POST['full_name']
        passenger_detail['date_of_journey'] = request.POST['date_of_journey']
        passenger_detail['age'] = request.POST['age']
        passenger_detail['gender'] = request.POST['gender']
        passenger_detail['preference'] = request.POST['preference']
        passenger_detail['with_child'] = request.POST['with_child']
        
        if passenger_detail['full_name'] == '' or passenger_detail['date_of_journey']  == '' or \
                 passenger_detail['age'] == ''  or passenger_detail['gender'] == ''  or \
                 passenger_detail['preference']  == '' or passenger_detail['with_child'] == '' :
            raise Http404("Please fill the complete detail")
        
        confirm_status_id = TicketStatus.objects.get(status_code = 'CNF' )
        confirm_ticket_count = TicketDetail.objects.filter(status_id = confirm_status_id ).count()
        if confirm_ticket_count < 24:
            #booking confirm ticket when confirm ticket are less then 24
            retval, msg, ticket_nbr = book_ticket_detail(confirm_status_id, passenger_detail)
        else:
            rac_status_id = TicketStatus.objects.get(status_code = 'RAC' )
            rac_ticket_count = TicketDetail.objects.filter(status_id = rac_status_id ).count()
            if rac_ticket_count < 8:
                #booking RAC ticket when all confirm ticket are booked and RAC tickets are available
                retval, msg, ticket_nbr = book_ticket_detail(rac_status_id, passenger_detail)
            else:
                #booking waiting list ticket here
                wl_status_id = TicketStatus.objects.get(status_code = 'WL' )
                wl_ticket_count = TicketDetail.objects.filter(status_id = rac_status_id ).count()
                if wl_ticket_count < 5:
                    retval, msg, ticket_nbr = book_ticket_detail(wl_status_id, passenger_detail)
                else:
                    raise Http404("Please fill the complete detail")
        response_data['ticket_nbr'] = ticket_nbr
        if not retval:
            if msg:
                raise Http404(msg)
            else:
                raise Http404('Error while booking ticket')
    return JsonResponse(response_data)

    
def book_ticket_detail(status_id, passenger_detail):
    if int(passenger_detail['age']) >= 5:
        if int(passenger_detail['age']) >= 60 or (passenger_detail['gender'] == 'FEMALE' and passenger_detail['with_child'].upper() == 'YES' ):
            berth_preference_id = BerthType.objects.get(berth_type = "LOWER")
            if TicketDetail.objects.filter(berth_type_id__berth_type = "LOWER").exists():
                return book_sheet(status_id, passenger_detail, berth_preference_id)
            else:
                return book_sheet(status_id, passenger_detail)
        else:
            return book_sheet(status_id, passenger_detail)
    else:
        save_passenger_data(passenger_detail)
        msg = "Can not book ticket for child with age less than 5 year"
        return True, msg, '' 


def book_sheet(status_id, passenger_detail, berth_preference_id=None):
    coach_list = Coach.objects.all().order_by("coach_nbr")
    if status_id.status_code in ['CNF','RAC']:
        for coach in coach_list:
            if status_id.status_code == 'CNF':
                if berth_preference_id: 
                    ticket_obj = TicketDetail.objects.filter(ticket_nbr__startswith = 'CNF',
                                                              coach_id = coach,
                                                              berth_type_id = berth_preference_id,
                                                              status_id__status_code = 'AVL',
                                                              date_of_journey = passenger_detail.get('date_of_journey')).first()
                else:
                    ticket_obj = TicketDetail.objects.filter(ticket_nbr__startswith = 'CNF',
                                                              coach_id = coach, 
                                                              status_id__status_code = 'AVL',
                                                              date_of_journey = passenger_detail.get('date_of_journey')).first()
            else:
                ticket_obj = TicketDetail.objects.filter(ticket_nbr__startswith = 'RAC',
                                                          coach_id = coach, 
                                                          status_id__isnull = True,
                                                          date_of_journey = passenger_detail.get('date_of_journey')).first()
                            
            if ticket_obj:
                if passenger_detail['gender'] == 'FEMALE' and not female_comfortability_check(coach, passenger_detail):
                    continue
                else:
                    break
    else:
        ticket_obj = TicketDetail.objects.filter(ticket_nbr__startswith = 'WL', 
                                                 status_id__isnull= True, 
                                                 date_of_journey = passenger_detail.get('date_of_journey')).first()
    
    if ticket_obj:       
        ticket_obj.status_id = status_id
        ticket_obj.save()
        save_passenger_data(passenger_detail, ticket_id = ticket_obj)
        return True, '', ticket_obj.ticket_nbr
    else:
        msg = 'There is no place for female in the coach/train'
        return False, msg, ''


def female_comfortability_check(coach, passenger_detail):
    """
    This will check if nay female can sit in the coach or not
    This function will take coach_nbr as input and will return False if all 7 ticket are booked for Male else this will return True
    """
    men_count = PassangerDetail.objects.filter(ticket_id__coach_id = coach, ticket_id__date_of_journey = passenger_detail['date_of_journey'], gender = 'MALE').count()
    if men_count >= 7:
        return False
    else:
        True


def save_passenger_data(passenger_detail, ticket_id = None):
    "This function will use to save the passanger details"
    berth_preference_id = BerthType.objects.get(berth_type = passenger_detail['preference'])
    child = PassangerDetail(name = passenger_detail['full_name'], 
                            age = passenger_detail['age'], 
                            gender = passenger_detail['gender'], 
                            berth_preference_id = berth_preference_id,
                            ticket_id = ticket_id)
    child.save()
    

def get_query_result(query):
    passanger_detail_list = None
    try:
        conn = psycopg2.connect(host="localhost",database="indian_railway_db", user="postgres", password="cwise",port='5432')
        print ("Connecting to database %s successful...")
        cur = conn.cursor()
        cur.execute(query)
        
        # display the PostgreSQL database server version
        passanger_detail_list = cur.fetchall()
        #print(passanger_detail_list)


        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return passanger_detail_list      


def print_booked_ticket(request):
    tday = datetime.date.today()
    query = """SELECT pd.name, pd.age, pd.gender ,pd.with_child, td.ticket_nbr, td.date_of_journey, bt.berth_type, ts.status_code, coach.coach_nbr
        FROM passanger_detail pd
        LEFT JOIN ticket_detail td ON pd.ticket_id = td.id
        LEFT OUTER JOIN berth_type bt ON td.berth_type_id = bt.id
        LEFT OUTER JOIN ticket_status ts ON td.status_id = ts.id
        LEFT OUTER JOIN coach ON td.coach_id = coach.id
        where td.date_of_journey = 'X_TODAY_X' and ts.status_code in ('CNF','RAC','WL')"""
    query = query.replace('X_TODAY_X', str(tday))
    print(query)
    passanger_detail_list = get_query_result(query)
    
    total_booked_ticket = len(passanger_detail_list)
    response_list = []
    for passanger_detail in passanger_detail_list:
        temp_dict = {}
        temp_dict["NAME"] = passanger_detail[0]
        temp_dict["AGE"] = passanger_detail[1]
        temp_dict["GENDER"] = passanger_detail[2]
        temp_dict["WITH_CHILD"] = passanger_detail[3]
        temp_dict["TICKET_NBR"] = passanger_detail[4]
        temp_dict["DATE_OF_JOURNEY"] = passanger_detail[5]
        temp_dict["BERTH_TYPE"] = passanger_detail[6]
        temp_dict["STATUS_CODE"] = passanger_detail[7]
        temp_dict["COACH_NBR"] = passanger_detail[8]
        response_list.append(temp_dict)
    
    return render(request, 'railway/booked_ticket.html', context = {'data': response_list,'total_booked_ticket':total_booked_ticket})


def print_available_ticket(request):
    tday = datetime.date.today()
    query = """SELECT td.ticket_nbr, td.date_of_journey, bt.berth_type, ts.status_code, coach.coach_nbr
        FROM ticket_detail td 
        LEFT OUTER JOIN berth_type bt ON td.berth_type_id = bt.id
        LEFT OUTER JOIN ticket_status ts ON td.status_id = ts.id
        LEFT OUTER JOIN coach ON td.coach_id = coach.id
        where td.date_of_journey = 'X_TODAY_X' and ts.status_code='AVL'"""
    query = query.replace('X_TODAY_X', str(tday))
    print(query)
    ticket_detail_list = get_query_result(query)
    
    total_available_ticket = len(ticket_detail_list)
    
    response_list = []
    for ticket_detail in ticket_detail_list:
        temp_dict = {}
        temp_dict["TICKET_NBR"] = ticket_detail[0]
        temp_dict["DATE_OF_JOURNEY"] = ticket_detail[1]
        temp_dict["BERTH_TYPE"] = ticket_detail[2]
        temp_dict["STATUS_CODE"] = ticket_detail[3]
        temp_dict["COACH_NBR"] = ticket_detail[4]
        response_list.append(temp_dict)
        
    return render(request, 'railway/available_ticket.html', context = {'data': response_list,'total_available_ticket':total_available_ticket})

