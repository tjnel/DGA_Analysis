import datetime as dt
from datetime import timedelta as td


# hard coded list of TLDs
tlds = ['.in', '.me', '.cc', '.su', '.tw', '.net', '.com', '.pw']
day_count = 1
domain_count = 10
seed = 0x65BA0743

#loops over the number of days to generate domains for
for i in range(day_count):
    # getting the seed date by adding x days to current datetime
    seed_date = dt.datetime.now()+td(days=i)
    # pulling out each date element
    tld_offset = int(seed_date.strftime('%d'))
    #gets day digit
    day = int(seed_date.strftime('%d'))
    #gets month digit
    month = int(seed_date.strftime('%m'))
    #gets year in 4 digit year format
    year = int(seed_date.strftime('%Y'))

    # Loop for number of domains to create per day
    for n in range(domain_count):
        # clears domain variable for next DGA
        domain = ""
        # DGA inner loop
        for y in range(14):
            '''
            Uses the algorithm from the http://www.johannesbader.ch/2015/05/the-dga-of-ranbyus/
            to create values that will be used to create the domains
            '''
            day = (day >> 15) ^ 16 * (day & 0x1FFF ^ 4 * (seed ^ day))
            year = ((year & 0xFFFFFFF0) << 17) ^ ((year ^ (7 * year)) >> 11)
            month = 14 * (month & 0xFFFFFFFE) ^ ((month ^ (4 * month)) >> 8)
            seed = (seed >> 6) ^ ((day + 8 * seed) << 8) & 0x3FFFF00
            # Calculates a char from algorithm values then adds to domain. Used ORD to convert 'a' to 97
            domain += chr(((day ^ month ^ year) % 25) + ord('a'))
        #adding TLD to domain
        domain = domain + tlds[tld_offset % 8]
        print("DGA for {} iteration num: {} is: {}".format(seed_date.strftime('%m/%d/%y'),n+1,domain))
        # adding 1 to the tld offset per offset++ in pseudo code
        tld_offset += 1