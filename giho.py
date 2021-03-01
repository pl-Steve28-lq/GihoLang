class Giho:
  def __init__(self, size=256):
    self.stack = []
    self.result = []
  
  def executePath(self, path):
    with open(path, encoding='utf-8') as f:
      code = f.read()
      return self.execute(code)
  
  def execute(self, code):
    self.__init__()
    code = self.filter(self.stripLine(code))
    length = len(code)
    idx = 0
    loop = self.findLoop(code)
    #print(code)
    while idx < length:
      ch = code[idx]
      #print(self.stack, self.result)

      if ch == '&': self.stack.append(1)
      if ch == '.' and self.stack: self.result.append(self.stack.pop())
      if ch == ',' and self.stack: self.stack.append(self.stack.pop() + self.stack.pop())
      if ch == '!' and self.result: self.result.pop()
      if ch == '?': self.stack.append(-1)
      if ch == '$' and self.result:
        self.stack.append(self.result.pop())
      if ch == '#':
        print(self.result[-1])
      if ch == '^':
        self.stack = list(reversed(self.stack))
      if ch == '`' and self.stack:
        ind = self.result.pop()-1
        self.result.append(self.stack[ind])
      if ch == '\n':
        self.stack.append(int(input()))
      
      if ch == '(' and self.stack[-1] <= 0:
        idx = loop[idx]-1
      if ch == ')' and self.stack[-1] > 0:
        idx = loop[idx]-1
      if ch in '\'"':
        l = loop[idx]
        if (
          (l[1] == 'left' and self.stack[-1] <= 0) or
          (l[1] == 'right' and self.stack[-1] > 0)
        ): idx = loop[idx]-1
      
      idx += 1
    return [self.stack, self.result]
  
  def findLoop(self, code):
    st = []
    res = {}
    for i in range(len(code)):
      ch = code[i]
      if ch == '(': st.append([i, ch])
      if not st: continue
      s = st[-1]
      if ch == ')':
        if s[1] == '(':
          p = st.pop()
          res[p[0]] = i
          res[i] = p[0]
      if ch in '\'"':
        if s[1] == ch:
          p = st.pop()
          res[p[0]] = [i, 'left']
          res[i] = [p[0], 'right']
        else:
          st.append([i, ch])
    return res     
  
  def filter(self, code):
    res = ''
    code = self.replAll(code, {
      '   ': '^', '  ': '&', ' .': '#', ' ,': '$', ' !': '`', '\n ': ''
    })
    for ch in code:
      if ch in '.,!?()\'"\n^#$`&':
        res += ch
    return self.replAll(res, {
      '()': '', '""': '', '\'\'': ''
    })

  def replAll(self, targ, info):
    for i in info:
      targ = targ.replace(i, info[i])
    return targ
  
  def strip(self, targ, k):
    if not targ: return targ
    while True:
      if targ[0] != k: break
      targ = targ[1:]
    while True:
      if targ[-1] != k: break
      targ = targ[:-1]
    return targ
  
  stripLine = lambda self, targ: self.strip(self, targ, '\n')

  def simplify(self, code, rep='|'):
    filt = { '   ': '^', '  ': '&', ' .': '#', ' ,': '$', ' !': '`', '\n ': '' }
    code = self.replAll(code, filt)
    res = ''
    for i in code:
      if i in '.,!?()\'"\n':
        res += i
      if i in filt.values():
        res += f'{rep}{list(filt.keys())[list(filt.values()).index(i)]}'
    return self.strip(res, rep)
