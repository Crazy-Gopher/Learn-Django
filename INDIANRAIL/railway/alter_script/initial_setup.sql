BEGIN;

INSERT INTO berth_type (berth_type, description) VALUES ('LOWER','Lower Sheet');
INSERT INTO berth_type (berth_type, description) VALUES ('MIDDLE','Middle Sheet');
INSERT INTO berth_type (berth_type, description) VALUES ('UPPER','Upper Sheet');
INSERT INTO berth_type (berth_type, description) VALUES ('SIDE','Side Sheet');


INSERT INTO coach (coach_nbr, description) VALUES ('S1','Sleeper Coach 1');
INSERT INTO coach (coach_nbr, description) VALUES ('S2','Sleeper Coach 2');
INSERT INTO coach (coach_nbr, description) VALUES ('S3','Sleeper Coach 3');
INSERT INTO coach (coach_nbr, description) VALUES ('S4','Sleeper Coach 4');


INSERT INTO ticket_status (status_code, description) VALUES ('AVL','Available');
INSERT INTO ticket_status (status_code, description) VALUES ('CNF','Confirmed');
INSERT INTO ticket_status (status_code, description) VALUES ('RAC','Reservation Againest Cancellation');
INSERT INTO ticket_status (status_code, description) VALUES ('WL','Waiting list');
INSERT INTO ticket_status (status_code, description) VALUES ('CAN','Cancelled');

INSERT INTO seq_counter (counter_nbr, counter_code) VALUES (0,'TICKET');

COMMIT;