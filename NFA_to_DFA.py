class NFAClass : #NFA class
   def __init__(self):
      self.N_symbols = list(map(int,input("NFA input symbol(정수)를 입력하세요:").split()))
      self.N_states = input("NFA state(문자)를 입력하세요:").split()
      self.N_finalState = input("final state(문자)를 입력하세요:").split()
      while set(self.N_finalState) & set(self.N_states) != set(self.N_finalState):
         print("NFA state에 없는 state입니다.")
         self.N_finalState = input("final state(문자)를 입력하세요:").split()
      self.N_table = [[0] * len(self.N_symbols) for _ in range(len(self.N_states))] # NFA table 초기화

      # δ table 입력받기
      for i in range(len(self.N_states)):
         for j in range(len(self.N_symbols)):
            print("δ : state[%c] symbol[%d] =>" % (self.N_states[i],self.N_symbols[j]), end=" ")
            temp= sorted(input().split())
            self.N_table[i][j] = temp
            while set(self.N_table[i][j]) & set(self.N_states) != set(self.N_table[i][j]):
               print("NFA state에 없는 state입니다.")
               print("δ : state[%c] symbol[%d] =>" % (self.N_states[i], self.N_symbols[j]), end=" ")
               temp = sorted(input().split()) # 정렬하여 입력
               self.N_table[i][j] = temp

   def printTable(self): # table 출력
      print("NFA TABLE")
      print("δ |", end=" ")
      for i in self.N_symbols:
         print("{0:^15}".format(i), end=" ")
      print("\n-----------------------------------")
      for i in range(len(self.N_states)):
         print(self.N_states[i], end=" | ")
         for j in range(len(self.N_symbols)):
            print("{0:^15}".format(str(self.N_table[i][j])), end=" ")
         print()
      print("Final state => ", end=" ")
      for f in self.N_finalState:
         print("{0:^5}".format(f), end=" ")
      print()

class Convert_NFA_to_DFA:
   def __init__(self,table,states,symbols,finalState):
      self.D_table = [[0] * len(symbols)] # DFA table 초기화
      self.D_states = [states[0]]  # start state 우선 추가
      self.D_symbols = symbols  #NFA state 와 같음
      self.D_finalState = [] # 종결상태 초기화
      state_ptr = 0 # DFA state에서 변환하고 있는 state의 index

      for i in range(len(self.D_symbols)): #start state 그대로 추가
         self.D_table[0][i] = table[0][i]
         if table[0][i] not in self.D_states: # D_state 중복제거
            self.D_states.append(table[0][i])
      state_ptr += 1

      while state_ptr < len(self.D_states): # D_state에 있는 모든 state를 완료할 때까지
         state_arr=[] # state에 대한 모든 symbol의 δ 값의 배열
         for i in range(len(self.D_symbols)):
            arr=[] # symbol의 δ 값의 배열
            for j in self.D_states[state_ptr]:
               for k in table[states.index(j)][i]:
                  if k not in arr: # 중복제거
                     arr.extend(k)
            arr.sort() # 알파벳 순서로 정렬
            state_arr.append(arr)
            if arr not in self.D_states: # D_state 중복제거
               #if len(arr)!=0:
               self.D_states.append(arr)
         self.D_table.append(state_arr) # D_state 열 추가
         state_ptr += 1 # 다음 D_state index

      for i in self.D_states: # final state 중 하나라도 포함하고 있다면
         if set(finalState) & set(i) :
            self.D_finalState.append(i);

   def printTable(self): # table 출력
      print("\nDFA TABLE")
      print("{0:^20}".format('δ') , end=" | ")
      for i in self.D_symbols:
         print("{0:^20}".format(i), end="   ")
      print("\n------------------------------------------------------------------")
      for i in range(len(self.D_states)):
         print("{0:^20}".format(str(self.D_states[i])), end=" | ")
         for j in range(len(self.D_symbols)):
            print("{0:^20}".format(str(self.D_table[i][j])), end="   ")
         print()
      print("Final state => ", end=" ")
      for f in self.D_finalState:
         print("{0:^15}".format(str(f)), end=" ")
      print()

class simple_DFA:
   def __init__(self,table,states,symbols,finalState):
      self.dfa_table = [[0] * len(symbols) for _ in range(len(states))] # 0으로 초기화
      self.dfa_states = []
      self.dfa_symbols = symbols
      self.dfa_finalState = []

      # 기존 DFA Table을 우선 ABCD로 나타내기
      for i in range(len(states)):
         self.dfa_states.append(chr(65 + i)) # 'A' 부터 시작
      for i in range(len(states)):
         for j in range(len(symbols)):
            self.dfa_table[i][j]=chr(65+states.index(table[i][j]))
      for i in range(len(finalState)):
         self.dfa_finalState.append(chr(65+states.index(finalState[i])))

   def printTable(self): # table 출력
      print("\nDFA TABLE(simple)")
      print("{0:^5}".format('δ'), end=" | ")
      for i in self.dfa_symbols:
         print("{0:^5}".format(i), end=" ")
      print("\n------------------------------")
      for i in range(len(self.dfa_states)):
         print("{0:^5}".format(self.dfa_states[i]), end=" | ")
         for j in range(len(self.dfa_symbols)):
            print("{0:^5}".format(self.dfa_table[i][j]), end=" ")
         print()
      print("Final state => ", end=" ")
      for f in self.dfa_finalState:
         print("{0:^5}".format(f), end=" ")
      print()

class Min_DFA:
   def __init__(self,table,states,symbols,finalState):
      self.min_dfa_table = [[0] * len(symbols) for _ in range(len(states))]
      self.min_dfa_symbols = symbols
      self.min_dfa_states = []
      self.min_dfa_finalState = []

      self.stateGroup = [] # 분할한 state 을 저장하는 배열
      self.new_table = [] # input symbol에 따라 분할한 state 중 몇번째 state로 가는지

      # final/non-final 나누어서 stateGroup 만들기
      non_final = []
      final = []
      for i in states:
         if i not in finalState:
            non_final.append(i)
         else:
            final.append(i)
      self.stateGroup.append(non_final)
      self.stateGroup.append(final)

      while True: # 분할이 더 이상 일어나지 않을 때까지
         # new_table 생성
         self.new_table=[] # table 초기화
         for i in symbols:
            arr=[] # symbol에 대한 모든 stateGroup(arr1)을 저장
            for j in self.stateGroup:
               arr1=[] # 한 stateGroup
               for k in j:
                  index=0
                  # stateGroup index 찾기
                  for idx, _i in enumerate(self.stateGroup):
                     for _j in _i:
                        if _j == table[states.index(k)][i]:
                           index=idx+1
                  arr1.append(index)
               arr.append(arr1)
            self.new_table.append(arr)

         # new_table 출력
         print()
         print("    ",end="")
         print(self.stateGroup)
         print("-------------------------------------------------------")
         for i in range(len(symbols)):
            print("{0:^4}".format(symbols[i]), end=" | ")
            print(self.new_table[i])

         # stateGroup 분할하기
         partition = 0 # 분할이 일어나면 1
         for j in range(len(self.stateGroup)):
            partition2 = 0 # 분할이 일어나면 1
            for i in range(len(symbols)):
               part1 = [] # 분할 part1
               part2 = [] # 분할 part1 : 비어있다면 분할 X
               arr1 = [] # 분할 state1
               arr2 = [] # 분할 state2
               partition3 = 0 # 분할이 일어나면 1
               for k in range(len(self.stateGroup[j])):
                  if k==0: # 첫번째라면 우선 part1, arr1에 저장
                     part1.append(self.new_table[i][j][k])
                     arr1.append(self.stateGroup[j][k])
                  else: # 두번째부터
                     if part1[-1]==self.new_table[i][j][k]:
                        part1.append(self.new_table[i][j][k])
                        arr1.append(self.stateGroup[j][k])
                     else: # 다른 state로 가는 경우 분할 해야함
                        partition3 = 1 #분할 O
                        part2.append(self.new_table[i][j][k])
                        arr2.append(self.stateGroup[j][k])
               if partition3: #분할 O
                  del self.stateGroup[j]
                  self.stateGroup.append(arr1)
                  self.stateGroup.append(arr2)
                  self.stateGroup.sort()
                  partition2=1
                  break
            if partition2: #분할 O
               partition = 1
               break
         if not partition: # 분할이 일어나지 않은 경우 while break
            break

      # new_table을 간소화하여 min_DFA의 state, symbol, table, final symbol에 대입
      for i in range(len(self.stateGroup)):
         for j in finalState: #final state
            if j in self.stateGroup[i]:
               if chr(97 + i) not in self.min_dfa_finalState: # 중복 제거
                  self.min_dfa_finalState.append(chr(97 + i))
         self.min_dfa_states.append(chr(97 + i))
      for i in range(len(self.min_dfa_symbols)):
         for j in range(len(self.stateGroup)):
            self.min_dfa_table[j][i] = chr(97 + self.new_table[i][j][0] -1)

   def printTable(self): #table 출력
      print("\nDFA TABLE(Reduced)")
      print("{0:^5}".format('δ'), end=" | ")
      for i in self.min_dfa_symbols:
         print("{0:^5}".format(i), end=" ")
      print("\n------------------------")
      for i in range(len(self.min_dfa_states)):
         print("{0:^5}".format(self.min_dfa_states[i]), end=" | ")
         for j in range(len(self.min_dfa_symbols)):
            print("{0:^5}".format(self.min_dfa_table[i][j]), end=" ")
         print()
      print("Final state => ", end=" ")
      for f in self.min_dfa_finalState:
         print("{0:^5}".format(f), end=" ")
      print()

if __name__=="__main__":
   nfa = NFAClass()
   nfa.printTable()
   dfa = Convert_NFA_to_DFA(nfa.N_table, nfa.N_states, nfa.N_symbols, nfa.N_finalState)
   dfa.printTable()
   simple_dfa = simple_DFA(dfa.D_table, dfa.D_states, dfa.D_symbols, dfa.D_finalState)
   simple_dfa.printTable()
   min_dfa=Min_DFA(simple_dfa.dfa_table, simple_dfa.dfa_states, simple_dfa.dfa_symbols, simple_dfa.dfa_finalState)
   min_dfa.printTable()
