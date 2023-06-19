def meetingRoom(s, f):
    meetings = list(zip(s, f)) 
    meetings.sort(key=lambda x: (x[1], x[0]))

    count = 1 
    endTime = meetings[0][1] 
    for i in range(1, len(meetings)):
        if meetings[i][0] >= endTime:
            count += 1
            endTime = meetings[i][1]

    return count

s = [1, 3], f = [3, 5]
meetingRoom(s,f)