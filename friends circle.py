A = [[1,1,0],
 [1,1,0],
 [0,0,1]]

def solution(A):
    seen = set()

    # the function find all people in circle of person_i
    def circle(person_i):
        for friend_id, value in enumerate(A[person_i]):
            if value == 1 and friend_id not in seen:
                seen.add(friend_id)
                circle(friend_id)

    # for person id from 1...N, every time find a new person haven't been already in the
    # current friend circle, add the circle number
    result = 0
    for i in range(len(A)):
        if i not in seen:
            circle(i)
            result += 1

    return result