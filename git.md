## git开发规范
采用单master分支(先不考虑多分支后续需要再拉分支)，本地代码只有测试通过后才能push到远端master
### 首次
1. 拉远程master分支

        git clone http://git.code.oa.com/ryanxjli/videotest.git

2. 本地拉自己的分支

        git checkout -b videotest-ryan


### 日常开发
1. 切换到本地分支

        git checkout videotest-ryan

2. 开发功能

3. 提交到本地分支

        git add .
        git commit -m "XXX"

4. 合并到本地master

        git checkout master 先切换到master分支
        git pull 拉线上最新代码
        git checkout videotest-ryan
        git merge master
        如果有冲突， 解决冲突， 然后git add, git commit到本地master

5. 提交到远端仓库

        git push origin videotest-ryan:videotest-ryan

6. 网页端发起

    merge request

7. 删除本地分支

    git branch -d videotest-ryan

### 回滚常用操作
1. 改乱了工作区，回滚工作区
git checkout -- XXX.py 工作区回滚到暂存区或仓库的状态
                                                                                                                                 
2. 回滚已经提交到暂存区的内容
git reset HEAD XXX.py 暂存区回滚到仓库中的状态
git checkout -- XXX.py 工作区回滚到暂存区的状态

3. 回滚已提交到本地仓库的修改
git log 查看要回滚的commit_id
git reset --hard commit_id 回滚