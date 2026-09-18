#!/usr/bin/env python3
"""Module 6: git-workflow — lessons + practices + checkpoint."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i2py import write_module, write_lesson, write_checkpoint

MOD = "git-workflow"

write_module(
    MOD,
    "Professional Git & Workflow",
    "Git as a professional tool: history as a graph, branches that stay mergeable, recovery without panic, and a review-driven workflow your team can trust.",
    "Git & Quy trình chuyên nghiệp",
    "Git như một công cụ chuyên nghiệp: lịch sử là một đồ thị, branch luôn merge được, khôi phục không hoảng loạn, và quy trình review mà cả team tin tưởng.",
    ["git-history-internals", "branching-strategies", "merge-vs-rebase", "recovering-commits", "github-flow-review", "secrets-and-env", "workflow-checkpoint"],
    ["history-practice", "branching-practice", "conflict-practice", "recovery-practice", "review-practice", "secrets-practice"],
)

write_lesson(
    MOD, "git-history-internals",
    "Git Internals: History as a Graph",
    "Commits are snapshots linked by parents — not diffs. Understanding the graph makes every Git command predictable.",
    20,
    """You already use `git commit` daily. Now look at what it actually creates.

## Commits are snapshots, not diffs

Each commit stores a full tree (snapshot) of every file, a message, an author, and a pointer to its **parent** commit(s). History is a directed graph:

```text
A ← B ← C        (main, linear)
      \\
       D ← E      (feature, diverged from B)
```

`HEAD` points to a branch; a branch is just a movable pointer to one commit. That is *all* a branch is — 41 bytes in `.git/refs`.

## Reading the graph

```bash
git log --oneline --graph --all
```

Learn to read this fluently. Questions professionals ask of history:

- **Where did these two lines diverge?** `git merge-base main feature`
- **Which commits are on main but not here?** `git log main ^feature` (read: commits reachable from main, excluding feature)
- **What exactly changed in commit X?** `git show X`
- **When did this line last change?** `git blame -L 10,20 file` — and `git log -S "thatString"` to find the commit that *introduced* it (pickaxe search).

## Branch pointers move; commits are (mostly) forever

When you "delete" a commit from a branch, the commit object still exists — the branch pointer simply stopped pointing at it. `git reflog` records every movement of HEAD for ~90 days, which is why almost nothing in Git is truly lost.

## Three states, one mental model

- **working directory** — your files right now
- **staging area (index)** — the *next* snapshot, built with `git add`
- **repository (HEAD)** — committed history

`git diff` (working vs index), `git diff --staged` (index vs HEAD), `git diff main` (working vs main). Professionals always check `git status` before any history-changing command.""",
    "Git nội bộ: Lịch sử là một đồ thị",
    "Mỗi commit là một snapshot đầy đủ liên kết với commit cha — không phải diff. Hiểu đồ thị giúp mọi lệnh Git trở nên dễ đoán.",
    """Bạn dùng `git commit` mỗi ngày. Giờ hãy xem nó thực sự tạo ra gì.

## Commit là snapshot, không phải diff

Mỗi commit lưu toàn bộ cây (snapshot) của mọi file, một message, tác giả, và một con trỏ trỏ tới commit **cha**. Lịch sử là một đồ thị có hướng:

```text
A ← B ← C        (main, tuyến tính)
      \\
       D ← E      (feature, tách ra từ B)
```

`HEAD` trỏ tới một branch; branch chỉ là một con trỏ di động trỏ vào một commit. Branch *chỉ* có vậy — 41 byte trong `.git/refs`.

## Đọc đồ thị

```bash
git log --oneline --graph --all
```

Hãy học đọc thành thạo. Những câu hỏi dân chuyên nghề hỏi về lịch sử:

- **Hai nhánh này tách nhau từ đâu?** `git merge-base main feature`
- **Commit nào có trên main mà nhánh này chưa có?** `git log main ^feature` (đọc: commit với tới được từ main, loại trừ feature)
- **Commit X chính xác thay đổi gì?** `git show X`
- **Dòng này thay đổi lần cuối khi nào?** `git blame -L 10,20 file` — và `git log -S "chuỗi đó"` để tìm commit *đã đưa vào* chuỗi đó (pickaxe search).

## Con trỏ branch di chuyển; commit gần như là vĩnh viễn

Khi bạn "xóa" một commit khỏi branch, commit object vẫn tồn tại — con trỏ branch đơn giản là ngừng trỏ tới nó. `git reflog` ghi lại mọi chuyển động của HEAD trong ~90 ngày, đó là lý do gần như không gì trong Git bị mất thật sự.

## Ba trạng thái, một mô hình tinh thần

- **working directory** — file của bạn ngay bây giờ
- **staging area (index)** — snapshot *tiếp theo*, được dựng bằng `git add`
- **repository (HEAD)** — lịch sử đã commit

`git diff` (working vs index), `git diff --staged` (index vs HEAD), `git diff main` (working vs main). Người chuyên nghiệp luôn kiểm tra `git status` trước bất kỳ lệnh nào thay đổi lịch sử.""",
)

write_lesson(
    MOD, "branching-strategies",
    "Branching Strategies That Scale",
    "Short-lived feature branches, trunks that stay releasable — comparing GitHub Flow, Git Flow, and trunk-based development.",
    18,
    """Branching strategy = the team's agreement about where code lives while it is being written.

## GitHub Flow (the default for most web teams)

1. Branch from `main` for each change: `feat/search-filters`
2. Commit small, push, open a **pull request**
3. Review + CI must pass
4. Merge to `main`, delete the branch, deploy

One long-lived branch (`main`), everything else short-lived. Ideal for continuously-deployed web apps — and what this course's projects use.

## Git Flow

Long-lived `main` (releases) + `develop` (integration), with `feature/`, `release/`, `hotfix/` branches. Powerful for versioned, scheduled-release software (mobile apps, installed products) — heavy for web.

## Trunk-based development

Everyone commits to `main` (or very short branches merged within a day). Incomplete features ship dark, behind **feature flags**:

```js
if (flags.newCheckout) renderNewCheckout();
else renderLegacyCheckout();
```

Requires strong tests and CI; eliminates merge pain entirely. Common at high-cadence teams.

## Choosing

| Signal | Fit |
|---|---|
| Deploy on every merge | GitHub Flow |
| Scheduled releases, versions | Git Flow |
| Many engineers, one product | Trunk-based + flags |
| Solo project | GitHub Flow, small branches |

Whatever you choose, the rule that matters: **branches live short.** The longer a branch diverges, the more its merge cost grows — the classic "merge hell" is a symptom of long-lived branches, not of Git.""",
    "Chiến lược branch có khả năng mở rộng",
    "Feature branch sống ngắn, trunk luôn ở trạng thái phát hành được — so sánh GitHub Flow, Git Flow và trunk-based development.",
    """Chiến lược branch = thỏa thuận của cả team về việc code nằm ở đâu trong lúc đang viết.

## GitHub Flow (mặc định cho phần lớn team web)

1. Tách branch từ `main` cho mỗi thay đổi: `feat/search-filters`
2. Commit nhỏ, push, mở **pull request**
3. Review + CI phải pass
4. Merge vào `main`, xóa branch, deploy

Một branch sống lâu (`main`), mọi thứ khác sống ngắn. Lý tưởng cho web app deploy liên tục — và là mô hình cho các project trong khóa học này.

## Git Flow

`main` (phát hành) + `develop` (tích hợp) sống lâu, kèm các branch `feature/`, `release/`, `hotfix/`. Mạnh cho phần mềm phát hành theo phiên bản định kỳ (mobile app, phần mềm cài đặt) — nhưng nặng nề cho web.

## Trunk-based development

Mọi người commit thẳng vào `main` (hoặc branch rất ngắn, merge trong ngày). Feature chưa hoàn thành được ship ẩn, sau **feature flag**:

```js
if (flags.newCheckout) renderNewCheckout();
else renderLegacyCheckout();
```

Đòi hỏi test mạnh và CI tốt; xóa sổ nỗi đau merge hoàn toàn. Phổ biến ở team có nhịp deploy cao.

## Cách chọn

| Tín hiệu | Phù hợp |
|---|---|
| Deploy ngay khi merge | GitHub Flow |
| Phát hành định kỳ, theo version | Git Flow |
| Nhiều kỹ sư, một sản phẩm | Trunk-based + feature flag |
| Project cá nhân | GitHub Flow, branch nhỏ |

Dù chọn gì, quy tắc quan trọng nhất là: **branch phải sống ngắn.** Branch tách càng lâu, chi phí merge càng lớn — "merge hell" kinh điển là triệu chứng của branch sống lâu, không phải lỗi của Git.""",
)

write_lesson(
    MOD, "merge-vs-rebase",
    "Merge, Rebase, and Conflicts",
    "Two ways to integrate history: preserve it with merge, or rewrite it linear with rebase — and how to survive conflicts either way.",
    22,
    """Two branches diverged. How do you put them back together?

## `git merge`: preserve history

```bash
git checkout feature
git merge main
# or, from main:
git merge feature   # creates a merge commit if histories diverged
```

A merge commit has **two parents**. History shows exactly what happened: "these two lines of work were combined here." Non-destructive — safe on shared branches.

## `git rebase`: rewrite into a straight line

```bash
git checkout feature
git rebase main
```

Rebase replays *your* commits on top of the latest `main`, creating **new commit objects** (same changes, new IDs). Result: linear history, no merge commit. The cost: the old commits are abandoned — which is why the golden rule exists.

> **Golden rule: never rebase commits others have pulled.** Rebase rewrites IDs; everyone's copies of the "same" commits become duplicates. Rebase only commits that exist only on your machine (or coordinate explicitly).

The professional pattern:

```bash
# keep feature fresh without a noise merge commit
git fetch origin
git rebase origin/main
```

## Conflicts: a resolution algorithm, not a panic

A conflict happens when both branches changed the same lines. Git marks the file:

```text
<<<<<<< HEAD
const total = subtotal * 1.1;      // your side
=======
const total = subtotal + fee;      // incoming side
>>>>>>> main
```

Resolution procedure:

1. `git status` — list every conflicted file (resolve all of them)
2. Open each file; decide the **correct code for the product** — not "mine" or "theirs" reflexively; often the answer is a combination
3. Remove all three marker lines
4. `git add <file>` to mark resolved
5. Finish: `git merge --continue` or `git rebase --continue`
6. **Run the tests** before finishing — a conflict resolved textually can still be broken logically

Escape hatches: `git merge --abort` / `git rebase --abort` return you to the exact pre-operation state. During a rebase conflict loop, `git rebase --skip` drops the offending commit entirely.

## Which to use?

- Shared/public branches → merge (never rewrite what others have)
- Your own local feature branch → rebase onto main for a clean pull request
- Team convention decides the rest — consistency beats ideology""",
    "Merge, Rebase và Conflict",
    "Hai cách hợp nhất lịch sử: merge giữ nguyên lịch sử, rebase viết lại tuyến tính — và cách sống sót qua conflict theo cả hai đường.",
    """Hai branch đã tách nhau. Làm sao hợp nhất lại?

## `git merge`: giữ nguyên lịch sử

```bash
git checkout feature
git merge main
# hoặc, từ main:
git merge feature   # tạo merge commit nếu lịch sử đã phân kỳ
```

Merge commit có **hai cha**. Lịch sử thể hiện đúng những gì đã xảy ra: "hai dòng công việc này được hợp nhất tại đây." Không phá hủy — an toàn trên branch dùng chung.

## `git rebase`: viết lại thành đường thẳng

```bash
git checkout feature
git rebase main
```

Rebase phát lại các commit *của bạn* lên trên `main` mới nhất, tạo ra **commit object mới** (cùng thay đổi, ID mới). Kết quả: lịch sử tuyến tính, không có merge commit. Cái giá: các commit cũ bị bỏ lại — vì vậy mới có golden rule.

> **Golden rule: không bao giờ rebase những commit mà người khác đã pull.** Rebase viết lại ID; bản "cùng một commit" của mỗi người trở thành bản trùng lặp. Chỉ rebase những commit chỉ tồn tại trên máy bạn (hoặc phối hợp rõ ràng với cả team).

Mô hình chuyên nghiệp:

```bash
# giữ feature cập nhật mà không tạo merge commit nhiễu
git fetch origin
git rebase origin/main
```

## Conflict: một thuật toán xử lý, không phải cơn hoảng loạn

Conflict xảy ra khi cả hai branch cùng sửa những dòng giống nhau. Git đánh dấu file:

```text
<<<<<<< HEAD
const total = subtotal * 1.1;      // phía của bạn
=======
const total = subtotal + fee;      // phía bên kia
>>>>>>> main
```

Quy trình xử lý:

1. `git status` — liệt kê mọi file bị conflict (phải xử lý hết)
2. Mở từng file; chọn **code đúng cho sản phẩm** — không phản xạ "của tôi" hay "của họ"; thường đáp án là một kết hợp
3. Xóa cả ba dòng marker
4. `git add <file>` để đánh dấu đã xử lý
5. Kết thúc: `git merge --continue` hoặc `git rebase --continue`
6. **Chạy test** trước khi xong — conflict xử lý đúng về văn bản vẫn có thể sai về logic

Lối thoát: `git merge --abort` / `git rebase --abort` đưa bạn về đúng trạng thái trước khi thao tác. Trong vòng lặp conflict khi rebase, `git rebase --skip` bỏ hẳn commit gây lỗi.

## Dùng cái nào?

- Branch dùng chung/công khai → merge (không bao giờ viết lại cái người khác đã có)
- Feature branch riêng của bạn → rebase vào main để pull request sạch
- Quy ước team quyết định phần còn lại — nhất quán hơn quan trọng hơn ý thức hệ""",
)

write_lesson(
    MOD, "recovering-commits",
    "Recovering: Reset, Revert, Cherry-pick, Stash",
    "Undo is a spectrum: move a branch (reset), add an inverse (revert), lift a commit (cherry-pick), or park work (stash).",
    20,
    """"I broke it." — four tools, chosen by one question: **who else has seen this commit?**

## `git revert`: the shared-branch tool

Creates a **new commit** that applies the inverse changes:

```bash
git revert abc1234        # commits the undo of abc1234
```

History stays intact; everyone pulling gets the undo. The only safe undo for commits already pushed to a shared branch.

## `git reset`: move the branch pointer

```bash
git reset --soft HEAD~1   # undo commit, keep changes staged
git reset --mixed HEAD~1  # undo commit, keep changes unstaged (default)
git reset --hard HEAD~1   # undo commit AND discard the changes
```

Moves the branch and (hard) rewrites the working tree. Fine for **local, unpushed** work; dangerous on shared branches — and `--hard` can destroy uncommitted work (check `git stash` first).

## `git cherry-pick`: lift one commit

Take a single commit from another branch and apply it here:

```bash
git cherry-pick abc1234
```

Typical uses: pulling one bugfix forward to a release branch, or grabbing one commit off a messy branch.

## `git stash`: park work in progress

```bash
git stash push -m "wip: search filters"
git stash list
git stash pop      # reapply + remove; apply keeps the stash
```

For "I need a clean tree for 5 minutes," not for long-term storage — stashes have no history or review.

## The decision table

| Situation | Tool |
|---|---|
| Commit pushed, others pulled it | `revert` |
| Local commit, not pushed | `reset --soft` / `--mixed` |
| Commit on the wrong branch entirely | `cherry-pick` (+ reset there) |
| Need to switch context right now | `stash` |
| "Everything is on fire" | `git reflog` → find the last good state → `git reset --hard <sha>` |

## Reflog is the safety net

`git reflog` shows every position HEAD has held. Even after a `reset --hard`, the old commits are reachable:

```bash
git reflog
git reset --hard HEAD@{2}   # go back to where you were two moves ago
```

Practice recovering *before* you need to: break a branch in a scratch repo and repair it. Panic is the enemy; the graph is your friend.""",
    "Khôi phục: Reset, Revert, Cherry-pick, Stash",
    "Undo là một phổ: di chuyển branch (reset), thêm nghịch đảo (revert), bê một commit (cherry-pick), hoặc gửi tạm công việc (stash).",
    """"Tôi làm hỏng rồi." — bốn công cụ, chọn bằng một câu hỏi: **đã có ai khác thấy commit này chưa?**

## `git revert`: công cụ cho branch dùng chung

Tạo một **commit mới** áp dụng các thay đổi nghịch đảo:

```bash
git revert abc1234        # commit phần hoàn tác của abc1234
```

Lịch sử được giữ nguyên; ai pull cũng nhận được phần hoàn tác. Đây là cách hoàn tác an toàn duy nhất cho commit đã push lên branch dùng chung.

## `git reset`: di chuyển con trỏ branch

```bash
git reset --soft HEAD~1   # hoàn tác commit, giữ thay đổi trong staging
git reset --mixed HEAD~1  # hoàn tác commit, giữ thay đổi ngoài staging (mặc định)
git reset --hard HEAD~1   # hoàn tác commit VÀ xóa luôn thay đổi
```

Di chuyển branch và (với --hard) viết lại working tree. Ổn cho công việc **local, chưa push**; nguy hiểm trên branch dùng chung — và `--hard` có thể phá hủy công việc chưa commit (nên `git stash` trước đã).

## `git cherry-pick`: bê một commit

Lấy một commit duy nhất từ branch khác áp dụng vào đây:

```bash
git cherry-pick abc1234
```

Dùng điển hình: kéo một bản sửa lỗi sang branch release, hoặc lấy đúng một commit từ một branch lộn xộn.

## `git stash`: gửi tạm công việc đang dở

```bash
git stash push -m "wip: search filters"
git stash list
git stash pop      # áp dụng + xóa khỏi stash; apply giữ lại stash
```

Dành cho "tôi cần cây file sạch trong 5 phút", không phải kho lưu trữ dài hạn — stash không có lịch sử hay review.

## Bảng quyết định

| Tình huống | Công cụ |
|---|---|
| Commit đã push, người khác đã pull | `revert` |
| Commit local, chưa push | `reset --soft` / `--mixed` |
| Commit rơi nhầm branch | `cherry-pick` (+ reset ở branch cũ) |
| Cần đổi bối cảnh ngay lập tức | `stash` |
| "Mọi thứ đang cháy" | `git reflog` → tìm trạng thái tốt cuối → `git reset --hard <sha>` |

## Reflog là mạng an toàn

`git reflog` hiển thị mọi vị trí HEAD từng đứng. Ngay cả sau `reset --hard`, các commit cũ vẫn với tới được:

```bash
git reflog
git reset --hard HEAD@{2}   # quay lại nơi bạn đứng trước đó hai bước
```

Hãy luyện khôi phục *trước khi* cần: cố tình làm hỏng một branch trong repo thử nghiệm rồi sửa lại. Hoảng loạn là kẻ thù; đồ thị là bạn của bạn.""",
)

write_lesson(
    MOD, "github-flow-review",
    "PRs, Code Review, Conventional Commits",
    "The social layer of version control: pull requests that are reviewable, reviews that teach, and commit history that reads like a changelog.",
    20,
    """A pull request is a *conversation artifact*, not just a merge button.

## Anatomy of a reviewable PR

- **One idea per PR.** "Add search filters" — not "add search filters, upgrade bundler, fix three typos."
- **Small.** Review quality collapses beyond ~400 changed lines; if it's bigger, split it.
- **A description that does the reviewer's homework:** what changed, why, how to test it, screenshots for UI, "here's what I decided NOT to do and why."

## Reviewing: the reader's job is to improve the code and the author

Review for, in order: **correctness** (does it do what it claims, including edge cases), **tests** (would a regression be caught), **readability** (names, structure), **security/perf** (the module 8–9 lenses). Style nits belong in automated linting, not human review.

Comment phrasing that works:

- "This could break when `query` is empty — did you consider X?" (question, not verdict)
- "nit: rename `d` → `duration`" (explicitly non-blocking)
- Blocking comments say **why** it blocks: "This logs the token — must be removed before merge."

**Authors:** respond to every comment (fix, or explain why not), re-request review after pushing. Never force-push a PR that has active discussion without saying so.

## Conventional Commits

A format that makes history machine-diffable:

```text
<type>(<scope>)?: <description>

feat(auth): add password reset
fix(cart): prevent negative quantities
refactor(search): extract debounce hook
docs: update contribution guide
chore(deps): bump zod to 4.5.4
```

Common types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `chore`, `ci`. Breaking changes get `!` (`feat!:`) or a `BREAKING CHANGE:` footer. Benefits: auto-generated changelogs, version bumps from commit types, greppable history.

## Semantic Versioning

`MAJOR.MINOR.PATCH` — bump MAJOR on breaking changes, MINOR on new features, PATCH on fixes. Libraries live by semver; applications mostly don't need it (they ship, they don't get imported). Know which one you're writing.

## The workflow this course uses

1. `feat/<short-name>` branch from main
2. Small conventional commits as you go
3. PR with description + tests
4. Self-review your own diff *before* requesting review — you'll catch half the issues yourself
5. Merge, delete branch, pull main locally""",
    "PR, Code Review, Conventional Commits",
    "Lớp xã hội của quản lý phiên bản: pull request dễ review, review vừa sửa code vừa dạy người viết, và lịch sử commit đọc như một changelog.",
    """Pull request là một *tài liệu đối thoại*, không chỉ là nút merge.

## Bố cục của một PR dễ review

- **Một PR một ý tưởng.** "Thêm bộ lọc tìm kiếm" — không phải "thêm bộ lọc, nâng bundler, sửa ba lỗi chính tả."
- **Nhỏ.** Chất lượng review sụp đổ khi vượt ~400 dòng thay đổi; lớn hơn thì tách ra.
- **Mô tả làm sẵn phần bài tập của người review:** đổi gì, vì sao, test thế nào, ảnh chụp cho UI, "những gì tôi cố tình KHÔNG làm và vì sao."

## Reviewing: nhiệm vụ của người đọc là cải thiện code lẫn người viết

Review theo thứ tự ưu tiên: **tính đúng đắn** (có làm đúng như mô tả, kể cả edge case), **test** (regression có bị phát hiện không), **khả năng đọc** (đặt tên, cấu trúc), **bảo mật/hiệu năng** (qua lăng kính module 8–9). Nit về style nên để cho linter tự động, không phải review tay.

Cách bình luận hiệu quả:

- "Đoạn này có thể hỏng khi `query` rỗng — bạn có cân nhắc X không?" (câu hỏi, không phải phán xét)
- "nit: đổi tên `d` → `duration`" (nói rõ là không chặn)
- Bình luận chặn merge phải nói rõ **tại sao**: "Đoạn này log token — phải xóa trước khi merge."

**Người viết:** phản hồi mọi bình luận (sửa, hoặc giải thích vì sao không), yêu cầu review lại sau khi push. Không bao giờ force-push một PR đang có thảo luận mà không báo trước.

## Conventional Commits

Một định dạng giúp lịch sử máy đọc được:

```text
<type>(<scope>)?: <mô tả>

feat(auth): add password reset
fix(cart): prevent negative quantities
refactor(search): extract debounce hook
docs: update contribution guide
chore(deps): bump zod to 4.5.4
```

Các type phổ biến: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `chore`, `ci`. Breaking change dùng `!` (`feat!:`) hoặc footer `BREAKING CHANGE:`. Lợi ích: changelog tự động, bump version theo loại commit, lịch sử grep được.

## Semantic Versioning

`MAJOR.MINOR.PATCH` — tăng MAJOR khi breaking change, MINOR khi thêm tính năng, PATCH khi sửa lỗi. Thư viện sống bằng semver; ứng dụng thì đa phần không cần (chúng được ship chứ không bị import). Hãy biết bạn đang viết loại nào.

## Quy trình khóa học này dùng

1. Branch `feat/<tên-ngắn>` từ main
2. Commit conventional nhỏ trong lúc làm
3. PR có mô tả + test
4. Tự review diff của chính mình *trước khi* mời review — bạn sẽ tự phát hiện một nửa vấn đề
5. Merge, xóa branch, pull main về máy""",
)

write_lesson(
    MOD, "secrets-and-env",
    "Secrets, Environment Variables, and Repo Hygiene",
    "Configuration belongs to the environment, not the code — and a leaked secret is a security incident, not a style issue.",
    18,
    """## The rule

Code and configuration are different things. Code goes in the repo. **Configuration — anything that varies by environment or grants access — goes in environment variables, never in committed files.**

```bash
# .env  (gitignored — local only)
DATABASE_URL=postgres://localhost:5432/app_dev
API_KEY=sk-local-abc123
SESSION_SECRET=some-long-random-string
```

```js
// reading config in Node
const port = process.env.PORT ?? 3000;
```

Commit a `.env.example` (keys, no values) so teammates know what to configure. Never import config deep in your modules — read it at the entry point and pass it down; that keeps code testable (module 7).

## Why leaks are one-way doors

A secret pushed to a public repo is compromised *within minutes* — bots scan commits for API keys automatically. Even deleting the file in a later commit doesn't help: history keeps it. If a secret leaks: **revoke/rotate it immediately**, then clean up. Prevention:

- `.gitignore` from project day one (`node_modules/`, `.env`, `dist/`, editor dirs)
- Pre-commit secret scanners (`gitleaks`, `git-secrets`) as a team guardrail
- Prefer short-lived credentials where possible

## Recognizing leaks in diffs

Review eyes should catch:

```diff
+ const API_KEY = "sk-live-9f8e7d6c5b4a";
```

Patterns that scream "secret": long random strings, `key|token|secret|password` in a name, anything prefixed `sk-`, `AKIA` (AWS), `ghp_` (GitHub), `AIza` (Google). A "temporary" hardcoded key is permanent — someone will copy that line into production.

## Repo hygiene

- **README that earns its keep:** what it is, how to run it, how to test it, where config lives. The README is your project's first impression and its recovery manual.
- **No committed build artifacts** (`dist/`, `node_modules/`) — the lockfile *is* committed (reproducible installs), the build output is not.
- **Meaningful history:** small conventional commits (previous lesson) make `git bisect` and review possible.
- **Lockfiles and dependency changes:** a PR that bumps dependencies says *why* in its description — dependency drift is a security surface (module 9).

## Threat model in miniature

Ask of every config value: *who can read this, and what happens if they do?* A public repo read = the world. A teammate's machine read = one laptop compromise. Design so the worst case is "rotate one key," not "rebuild the account." """,
    "Secrets, biến môi trường và vệ sinh repo",
    "Cấu hình thuộc về môi trường, không phải code — và secret bị lộ là một sự cố bảo mật, không phải vấn đề phong cách.",
    """## Quy tắc

Code và cấu hình là hai thứ khác nhau. Code đưa vào repo. **Cấu hình — thứ gì đó thay đổi theo môi trường hoặc cấp quyền truy cập — đưa vào biến môi trường, không bao giờ commit vào file.**

```bash
# .env  (gitignored — chỉ dùng local)
DATABASE_URL=postgres://localhost:5432/app_dev
API_KEY=sk-local-abc123
SESSION_SECRET=chuoi-ngau-nhien-dai
```

```js
// đọc cấu hình trong Node
const port = process.env.PORT ?? 3000;
```

Commit một `.env.example` (chỉ key, không value) để đồng nghiệp biết cần cấu hình gì. Không bao giờ đọc config sâu trong module — đọc ở entry point rồi truyền xuống; giúp code dễ test (module 7).

## Vì sao lộ secret là cánh cửa một chiều

Secret push lên repo công khai sẽ bị xâm phạm *trong vài phút* — bot quét commit tìm API key tự động. Xóa file ở commit sau cũng vô ích: lịch sử vẫn giữ nó. Khi secret lộ: **thu hồi/xoay vòng ngay lập tức**, rồi mới dọn dẹp. Phòng bệnh:

- `.gitignore` từ ngày đầu dự án (`node_modules/`, `.env`, `dist/`, thư mục editor)
- Công cụ quét secret pre-commit (`gitleaks`, `git-secrets`) làm rào chắn của team
- Ưu tiên credential ngắn hạn khi có thể

## Nhận diện leak trong diff

Đôi mắt review cần tóm được:

```diff
+ const API_KEY = "sk-live-9f8e7d6c5b4a";
```

Mẫu đáng báo động: chuỗi ngẫu nhiên dài, tên chứa `key|token|secret|password`, tiền tố `sk-`, `AKIA` (AWS), `ghp_` (GitHub), `AIza` (Google). Key hardcode "tạm thời" là vĩnh viễn — ai đó sẽ copy dòng đó lên production.

## Vệ sinh repo

- **README xứng đáng tồn tại:** nó là gì, cách chạy, cách test, config nằm ở đâu. README là ấn tượng đầu tiên và là cẩm nang khôi phục của dự án.
- **Không commit sản phẩm build** (`dist/`, `node_modules/`) — lockfile *thì* commit (cài đặt tái lập được), output build thì không.
- **Lịch sử có nghĩa:** commit conventional nhỏ (bài trước) giúp `git bisect` và review khả thi.
- **Lockfile và thay đổi dependency:** PR bump dependency phải nói *lý do* trong mô tả — lệch phụ thuộc là một bề mặt bảo mật (module 9).

## Mô hình đe dọa thu nhỏ

Hỏi với mọi giá trị cấu hình: *ai đọc được nó, và điều gì xảy ra nếu họ đọc?* Repo công khai bị đọc = cả thế giới. Máy đồng nghiệp bị đọc = một laptop bị xâm phạm. Hãy thiết kế để trường hợp xấu nhất là "xoay một key", không phải "dựng lại toàn bộ tài khoản." """,
)

write_checkpoint(
    MOD, "workflow-checkpoint",
    "Checkpoint: Professional Workflow",
    "Prove you can read history, resolve conflicts logically, recover safely, and run a review-grade workflow.",
    20,
    """This checkpoint tests the *judgment* layer of Git — the part that separates someone who knows commands from someone who can run a professional workflow.

You will write pure functions that model real Git decisions. The sandbox can't run real Git; the reasoning is what we grade: conflict resolution semantics, recovery choices, and conventional-commit tooling.""",
    "Kiểm tra kiến thức: Quy trình chuyên nghiệp",
    "Chứng minh bạn đọc được lịch sử, xử lý conflict đúng logic, khôi phục an toàn, và vận hành quy trình đạt chuẩn review.",
    """Checkpoint này kiểm tra lớp *phán đoán* của Git — phần phân biệt người biết lệnh với người vận hành được quy trình chuyên nghiệp.

Bạn sẽ viết các hàm thuần mô phỏng quyết định Git thực tế. Sandbox không chạy Git thật; thứ bị chấm điểm là lập luận: ngữ nghĩa xử lý conflict, lựa chọn khôi phục, và công cụ conventional-commit.""",
    {
        "id": "i2-workflow-checkpoint",
        "title": "Workflow Simulator",
        "prompt": "Write THREE functions. 1) `resolveConflict(mine, theirs, strategy)` where mine/theirs are conflict-halved code strings and strategy is \"mine\", \"theirs\", or \"combine\": return mine for \"mine\", theirs for \"theirs\", and for \"combine\" the string `mine + \"\\n\" + theirs` (line-stacked). 2) `chooseRecovery(pushed, othersPulled, wantHistory)` — return \"revert\" when the commit was pushed AND others pulled it; return \"reset\" when it was not pushed; otherwise (pushed, nobody pulled, wantHistory true) return \"merge\"... but if pushed, not pulled, and wantHistory is false, return \"reset\". 3) `bumpVersion(version, type)` — given semver string \"MAJOR.MINOR.PATCH\" and conventional type, bump patch for \"fix\", minor for \"feat\", major for \"feat!\" or \"BREAKING CHANGE\"; return the new version string.",
        "difficulty": "intermediate",
        "level": "checkpoint",
        "boilerplate": "function resolveConflict(mine, theirs, strategy) {\n  // your code\n}\n\nfunction chooseRecovery(pushed, othersPulled, wantHistory) {\n  // your code\n}\n\nfunction bumpVersion(version, type) {\n  // your code\n}\n",
        "tests": [
            {
                "name": "conflict resolution follows the chosen strategy",
                "code": "const fn = new Function(code + \"\\nreturn { resolveConflict, chooseRecovery, bumpVersion };\");\nconst { resolveConflict } = fn();\nif (resolveConflict(\"a\", \"b\", \"mine\") !== \"a\") throw new Error(\"'mine' keeps our side.\");\nif (resolveConflict(\"a\", \"b\", \"theirs\") !== \"b\") throw new Error(\"'theirs' takes the incoming side.\");\nif (resolveConflict(\"a\", \"b\", \"combine\") !== \"a\\nb\") throw new Error(\"'combine' stacks both sides with a newline.\");",
                "hint": "Strategy is a simple branch — the lesson's point is that the CHOICE is deliberate, not that the code is hard.",
            },
            {
                "name": "recovery choices match the safety rules",
                "code": "const fn = new Function(code + \"\\nreturn { resolveConflict, chooseRecovery, bumpVersion };\");\nconst { chooseRecovery } = fn();\nif (chooseRecovery(true, true, true) !== \"revert\") throw new Error(\"Pushed + pulled => only revert is safe.\");\nif (chooseRecovery(false, false, true) !== \"reset\") throw new Error(\"Never pushed => reset is fine.\");\nif (chooseRecovery(true, false, true) !== \"merge\") throw new Error(\"Pushed, not pulled, history wanted => merge.\");\nif (chooseRecovery(true, false, false) !== \"reset\") throw new Error(\"Pushed, not pulled, history disposable => reset.\");",
                "hint": "Ordered checks: pulled? -> revert. Not pushed? -> reset. Then the history flag decides.",
            },
            {
                "name": "semver bumps follow commit types",
                "code": "const fn = new Function(code + \"\\nreturn { resolveConflict, chooseRecovery, bumpVersion };\");\nconst { bumpVersion } = fn();\nif (bumpVersion(\"1.2.3\", \"fix\") !== \"1.2.4\") throw new Error(\"fix bumps patch.\");\nif (bumpVersion(\"1.2.3\", \"feat\") !== \"1.3.0\") throw new Error(\"feat bumps minor and zeroes patch.\");\nif (bumpVersion(\"1.2.3\", \"feat!\") !== \"2.0.0\") throw new Error(\"Breaking changes bump major and zero minor+patch.\");\nif (bumpVersion(\"2.0.5\", \"BREAKING CHANGE\") !== \"3.0.0\") throw new Error(\"The BREAKING CHANGE footer behaves like '!'.\");",
                "hint": "Parse the three numbers, pick an index by type, increment it, zero everything after it.",
            },
        ],
    },
    {
        "id": "i2-workflow-checkpoint",
        "title": "Mô phỏng quy trình",
        "prompt": "Viết BA hàm. 1) `resolveConflict(mine, theirs, strategy)` với mine/theirs là hai nửa code bị conflict và strategy là \"mine\", \"theirs\" hoặc \"combine\": trả về mine cho \"mine\", theirs cho \"theirs\", và với \"combine\" trả về `mine + \"\\n\" + theirs` (xếp chồng dòng). 2) `chooseRecovery(pushed, othersPulled, wantHistory)` — trả về \"revert\" khi commit đã push VÀ người khác đã pull; trả về \"reset\" khi chưa push; nếu đã push, chưa ai pull và wantHistory true thì trả về \"merge\"... nhưng nếu đã push, chưa ai pull và wantHistory false thì trả về \"reset\". 3) `bumpVersion(version, type)` — nhận chuỗi semver \"MAJOR.MINOR.PATCH\" và loại conventional commit: \"fix\" tăng patch, \"feat\" tăng minor, \"feat!\" hoặc \"BREAKING CHANGE\" tăng major; trả về chuỗi version mới.",
        "tests": [
            {"name": "xử lý conflict theo chiến lược đã chọn", "hint": "Strategy chỉ là một nhánh đơn giản — điểm của bài là LỰA CHỌN phải có chủ đích."},
            {"name": "lựa chọn khôi phục đúng luật an toàn", "hint": "Kiểm tra theo thứ tự: đã bị pull? -> revert. Chưa push? -> reset. Cờ history quyết định phần còn lại."},
            {"name": "bump semver theo loại commit", "hint": "Tách ba số, chọn vị trí theo type, tăng nó, đặt 0 cho mọi số phía sau."},
        ],
    },
)

print("Module 6 lessons + checkpoint written.")
