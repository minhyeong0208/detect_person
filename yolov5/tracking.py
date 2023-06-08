import math
def person_tracker(Total_person):
    move_info=[]

    sum_person=Total_person[0][0]+Total_person[1][0]
    #A_frame_person=list(Total_person[0].values)
    #B_frame_person=list(Total_person[1].values)
    #sum_person=A_frame_person[0]+B_frame_person[0]
    move_info.append({0:"초기 탐지"})
    temp=sum_person
    for i in range(1,(min(len(Total_person[0]),len(Total_person[1])))):
        sum_person=Total_person[0][i]+Total_person[1][i] # i프레임에서 A,B의 전체 사람 수
        A_dif=Total_person[0][i]-Total_person[0][i-1] # A 카메라 i-1 >> i 프레임의 사람 변화수
        B_dif=Total_person[1][i]-Total_person[1][i-1] # B 카메라 i-1 >> i 프레임의 사람 변화수
        #sum_person=A_frame_person[i]+B_frame_person[i]
        #A_dif=A_frame_person[i]=A_frame_person[i-1]
        #B_dif=B_frame_person[i]=B_frame_person[i-1]
        
        ext=sum_person-temp
        if ext==0: #외부 이동 없음
            if A_dif==0:
                move_info.append({i:"변화 없음"})
            elif A_dif>0:
                move_info.append({i:f"A에서 B로 {A_dif}명 이동"})
            else:
                move_info.append({i:f"B에서 A로 {B_dif}명 이동"})

        elif (ext)>0: # 외부 유입
            if A_dif>B_dif: #
                move_info.append({i:f"B에서 A로 {abs(B_dif)}명 이동, 외부에서 A로 {abs(A_dif)-abs(B_dif)}명 이동"})
            else:
                move_info.append({i:f"A에서 B로 {abs(A_dif)}명 이동, 외부에서 B로 {abs(B_dif)-abs(A_dif)}명 이동"})
        
        else: # 외부 유출
            if A_dif>B_dif:
                move_info.append({i:f"B에서 A로 {abs(A_dif)}명 이동, B에서 외부로 {abs(B_dif)-abs(A_dif)}명 이동"})
            else:
                move_info.append({i:f"A에서 B로 {abs(B_dif)}명 이동, A에서 외부로 {abs(A_dif)-abs(B_dif)}명 이동"})

        temp=sum_person

    return move_info