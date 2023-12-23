from flask import Flask, render_template, request, abort
import random
app = Flask(__name__)

@app.route("/")
def mainpage(): return render_template("main.html")
@app.route("/m")
def mainpage_mobile(): return render_template("main_mobile.html")

@app.route("/generator")
def generator():
    errorText = """<div class="alert alert-danger" role="alert" id="errorwin"><errorText></div>"""
    try:
        randomList = []
        # 取得開始值，終止值，請求個數
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        count = int(request.args.get('count'))
        # 檢查: 請求個數必須大於0
        if count < 0: return abort(500)
        # 取得數字是否可以重複，並檢查
        repeat = request.args.get('repeat')
        if (repeat == None): repeat = True # 不能重複
        elif (repeat == "on"): repeat = False # 可以重複
        else: return abort(500)
        # 檢查: 起始數字小於終止數字；數字範圍大於等於要求個數
        if (start > end): return errorText.replace("<errorText>", '終止數字需比起始數字大 <a id="des" href="https://github.com/pictures2333/rng-cheat-website/blob/master/errDocument.md">err.01 說明文件</a>')
        if (abs(end-start)+1 < count and repeat): return errorText.replace("<errorText>", '數字範圍比要求的數字個數少 <a id="des" href="https://github.com/pictures2333/rng-cheat-website/blob/master/errDocument.md">err.02 說明文件</a>')

        # 取得排除值
        exclude = request.args.get('exclude')
        excludeList = []
        if (exclude != None): 
            if (len(exclude) <= 500): excludeList = list(set(list(map(int, exclude.split()))))
            else: return abort(500)
        # 挑出在範圍內的數字
        exclude2 = []
        for i in excludeList: 
            if (i >= start and i <= end): exclude2.append(i)
        # 如果數字不能重複: 檢查扣完這些數字之後剩下的範圍會不會太小
        if (abs(end-start)+1) - len(exclude2) < count and repeat == True: return errorText.replace("<errorText>", '數字範圍扣除要求排除的數字數目後小於要求數字個數 <a id="des" href="https://github.com/pictures2333/rng-cheat-website/blob/master/errDocument.md">err.03 說明文件</a>')
        # 如果數字可以重複: 檢查排除列表會不會把整個範圍內的數字都排除掉
        if len(exclude2) >= (abs(end-start)+1) and repeat == False: return errorText.replace("<errorText>", '數字範圍內的數字都被列入排除了 <a id="des" href="https://github.com/pictures2333/rng-cheat-website/blob/master/errDocument.md">err.04 說明文件</a>')

        # 取得必定包含值
        include = request.args.get('include')
        includeList = []
        if (include != None):
            if (len(include) <= 500): includeList = list(set(list(map(int, include.split()))))
            else: return abort(500)
        # 檢查所有數字是不是都在範圍內、是否跟排除列表衝突
        for i in includeList:
            if i > end or i < start: return errorText.replace("<errorText>", '必定包含數字超出數字範圍 <a id="des" href="https://github.com/pictures2333/rng-cheat-website/blob/master/errDocument.md">err.05 說明文件</a>')
            if len(exclude2) != 0 and i in exclude2: return errorText.replace("<errorText>", '必定包含數字和排除數字衝突 <a id="des" href="https://github.com/pictures2333/rng-cheat-website/blob/master/errDocument.md">err.06 說明文件</a>')
        # 檢查必定列表是否比要求數字列表多
        if len(includeList) > count: return errorText.replace("<errorText>", '必定包含數字個數超出要求數字個數 <a id="des" href="https://github.com/pictures2333/rng-cheat-website/blob/master/errDocument.md">err.07 說明文件</a>')
        # 如果沒有爆掉: 直接添加必定值到最終產生變數表
        randomList = includeList

        # 取亂數
        for i in range(count-len(includeList)):
            tRn = random.randint(start, end)
            while (repeat and (tRn in randomList) or (len(exclude2) != 0 and tRn in exclude2)): tRn = random.randint(start, end)
            randomList.append(tRn)
        # 確認是否排序
        tfSort = request.args.get('sort')
        if (tfSort == None): random.shuffle(randomList) # 加以打亂
        elif (tfSort == "on"): randomList.sort()
        else: return abort(500)
        # 開始組合字串
        finalTrans = ""
        for i in randomList: finalTrans += str(i) + "<br>"

        # 回傳
        return finalTrans
    except:
        return abort(500)

if __name__ == '__main__':
    app.run()