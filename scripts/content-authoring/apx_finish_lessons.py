#!/usr/bin/env python3
"""Writes the 72 teaching lessons (3 per module) for ap-csa-advanced.

Lesson BODIES live in the apx_mN.py generator scripts as L1/L2/L3 and
VI_L1/VI_L2/VI_L3 module-level variables; this script imports each module
(running its idempotent writes is harmless) and authors the lesson
metadata around those bodies.
"""
import importlib

import apx

# (module_dir, script_name, [(lesson_id, en_title, en_desc, vi_title, vi_desc)] x3)
PLAN = [
    ("apx-problem-solving", "apx_m1", [
        ("apx-m1-method", "The working method", "Restate, type the data, find boundaries, pick the smallest correct algorithm — the five-step method this course runs on.", "Phương pháp làm việc", "Diễn đạt lại, xác định kiểu dữ liệu, tìm biên, chọn thuật toán nhỏ nhất đúng — phương pháp năm bước của khóa học."),
        ("apx-m1-decompose", "Multi-concept decomposition", "Extract the computation hiding inside an unfamiliar story: what is stored, which words map to conditions, which words are decoration.", "Phân rã đa khái niệm", "Trích xuất phép tính ẩn trong một câu chuyện lạ: cái gì được lưu, từ nào ánh xạ thành điều kiện, từ nào chỉ là trang trí."),
        ("apx-m1-selective", "Trace or reason?", "Selective execution: state tables for state-heavy code, invariants for accumulators, boxes-and-arrows for references.", "Truy vết hay suy luận?", "Thực thi chọn lọc: bảng trạng thái cho mã nặng trạng thái, bất biến cho bộ tích lũy, hộp-và-mũi-tên cho tham chiếu."),
    ]),
    ("apx-tracing", "apx_m2", [
        ("apx-m2-tables", "State-table discipline", "One row per event, one column per changing value — and the two misdirections (dead variables, frozen values) that break traces.", "Kỷ luật bảng trạng thái", "Mỗi sự kiện một dòng, mỗi giá trị thay đổi một cột — và hai yếu tố đánh lạc hướng (biến chết, giá trị đóng băng) phá hỏng truy vết."),
        ("apx-m2-objects", "Objects, statics, and mutation", "Instance vs static ledgers, ArrayList removal shifts, and reference semantics under pass-by-value.", "Đối tượng, static, và biến đổi", "Sổ cái instance so với static, phép dồn khi xóa ArrayList, và ngữ nghĩa tham chiếu dưới truyền-theo-giá-trị."),
        ("apx-m2-invariants", "Nested loops as arithmetic", "Recognize the sum shapes (constant, series, halving) instead of simulating every pass — small-case simulation plus generalization.", "Vòng lặp lồng là phép tính", "Nhận diện các dạng tổng (không đổi, cấp số cộng, chia đôi) thay vì mô phỏng từng lượt — mô phỏng ca nhỏ cộng khái quát hóa."),
    ]),
    ("apx-mcq-lab", "apx_m3", [
        ("apx-m3-answers", "Predict before you look", "Read the stem first, predict without options, then match — and re-trace one specific step when nothing matches.", "Dự đoán trước khi nhìn", "Đọc đề trước, dự đoán không cần phương án, rồi đối chiếu — và truy vết lại một bước cụ thể khi không cái nào khớp."),
        ("apx-m3-misconceptions", "Distractors are diagnoses", "Every wrong option encodes a named misconception: off-by-one, shadowing, aliasing, immutability, dispatch, short-circuit.", "Phương án nhiễu là bản chẩn đoán", "Mọi phương án sai mã hóa một hiểu nhầm có tên: lệch-một, bóng che, bí danh, bất biến, điều phối, ngắn mạch."),
        ("apx-m3-explanations", "Explaining every distractor", "The highest-yield review: for each eliminated option, complete 'a student picks this if they believe X, but actually Y'.", "Giải thích từng phương án sai", "Ôn tập hiệu quả nhất: với mỗi phương án bị loại, hoàn thành 'học sinh chọn cái này nếu tin X, nhưng thực ra Y'."),
    ]),
    ("apx-speed", "apx_m4", [
        ("apx-m4-tempo", "The 90-second tempo", "Two-pass pacing: answer the visible, mark the rest, never let one trace exceed three minutes.", "Nhịp độ 90 giây", "Nhịp hai lượt: trả lời cái nhìn thấy được, đánh dấu phần còn lại, không bao giờ để một truy vết vượt ba phút."),
        ("apx-m4-elimination", "Elimination as arithmetic", "Kill options in order: type-impossible, bounds-impossible, trace-impossible — then pick the survivor needing no invisible code.", "Loại trừ là phép tính", "Loại phương án theo thứ tự: bất-khả-kiểu, bất-khả-biên, bất-khả-truy-vết — rồi chọn người sống sót không cần mã vô hình."),
        ("apx-m4-patterns", "Five patterns cover the exam", "Accumulator, search-and-flag, remove-scan, two-ledger, cast-then-compute — recognize the shape, know the trap.", "Năm mẫu phủ đề thi", "Bộ tích lũy, tìm-và-cắm-cờ, quét-xóa, hai-sổ-cái, ép-rồi-tính — nhận dạng hình dạng, biết cái bẫy."),
    ]),
    ("apx-strings", "apx_m5", [
        ("apx-m5-toolkit", "Index arithmetic toolkit", "The middle-two formula for both parities, adjacent comparison from index 1, and substring endpoints said out loud.", "Bộ công cụ phép toán chỉ số", "Công thức cặp-giữa cho cả hai tính chẵn lẻ, so sánh liền kề từ chỉ số 1, và hai đầu substring đọc thành tiếng."),
        ("apx-m5-boundaries", "Character classification and shifts", "Raw classification without imports, char arithmetic with wrap-around, and the pass-through rule for non-letters.", "Phân loại ký tự và phép dịch", "Phân loại thủ công không cần import, phép toán char với vòng-lại, và luật ký-tự-không-chữ đi qua nguyên bản."),
        ("apx-m5-transform", "Transformation pipelines", "Two clean passes beat one clever pass; run-length problems live or die on the final flush.", "Chuỗi biến đổi", "Hai lượt sạch thắng một lượt thông minh; bài run-length sống chết ở phép xả cuối."),
    ]),
    ("apx-arrays", "apx_m6", [
        ("apx-m6-twopass", "Two passes beat one clever pass", "Second-extremum problems decompose into find-max then find-max-excluding — mechanical under pressure.", "Hai lượt thắng một lượt thông minh", "Bài cực-trị-thứ-hai phân rã thành tìm-max rồi tìm-max-loại-trừ — máy móc dưới áp lực."),
        ("apx-m6-writeindex", "The write-index pattern", "In-place compaction with a write cursor: dedup, remove-matches, move-zeros — one pattern, every compact FRQ.", "Mẫu chỉ số ghi", "Nén tại chỗ bằng con trỏ ghi: dedup, xóa-khớp, dời-số-0 — một mẫu cho mọi FRQ nén."),
        ("apx-m6-almutation", "ArrayList mutation discipline", "Backward loops, build-a-new-list, and the forbidden for-each removal — plus the two-cursor merge drain phase.", "Kỷ luật biến đổi ArrayList", "Vòng ngược, dựng-danh-sách-mới, và phép xóa for-each bị cấm — cộng giai đoạn rút-cạn của trộn hai con trỏ."),
    ]),
    ("apx-grids", "apx_m7", [
        ("apx-m7-axes", "Rows, columns, and rotation", "g[r][c] always; g.length vs g[0].length; the 90° rotation derived once and verified on 2x3.", "Hàng, cột, và phép xoay", "Luôn luôn g[r][c]; g.length so với g[0].length; phép xoay 90° dẫn một lần và kiểm chứng trên 2x3."),
        ("apx-m7-neighborhood", "Neighborhood processing", "Offset tables plus bounds guards; the two spec decisions (count self? divide by 8 or by actual?) that hide difficulty.", "Xử lý vùng lân cận", "Bảng độ dịch cộng biến chặn biên; hai quyết định đặc tả (tự đếm? chia cho 8 hay số thực?) giấu độ khó."),
        ("apx-m7-bounds", "Complex traversals are boundary management", "Spirals with four shrinking walls and re-checks; test 1xn, nx1, and 1x1 before anything else.", "Duyệt phức tạp là quản lý biên", "Xoắn ốc với bốn bức tường thu nhỏ và kiểm tra lại; thử 1xn, nx1, và 1x1 trước mọi thứ khác."),
    ]),
    ("apx-oop", "apx_m8", [
        ("apx-m8-state", "Objects are state machines", "Fields are state, methods are transitions; the FRQ2 shape is one guard, one boundary, one accessor.", "Đối tượng là máy trạng thái", "Trường là trạng thái, phương thức là bước chuyển; hình dạng FRQ2 là một biến chặn, một biên, một accessor."),
        ("apx-m8-helpers", "Helpers and constructor traps", "Named helpers earn rubric rows; shadowed parameters and forgotten fields poison every later call.", "Helper và bẫy constructor", "Helper được đặt tên giành dòng bảng điểm; tham số bị bóng che và trường bị quên đầu độc mọi lời gọi sau."),
        ("apx-m8-interaction", "Designing from a spec", "One method per spec bullet, guards stated in one sentence, and every transition driven to every boundary.", "Thiết kế từ đặc tả", "Mỗi gạch đầu dòng một phương thức, biến chặn nêu trong một câu, và mọi bước chuyển đưa tới mọi biên."),
    ]),
    ("apx-polymorphism", "apx_m9", [
        ("apx-m9-two-types", "Two answers in one variable", "Reference type governs what you may name; object type governs what runs; fields dispatch by neither.", "Hai đáp án trong một biến", "Kiểu tham chiếu cai trị cái bạn được gọi tên; kiểu đối tượng cai trị cái chạy; trường không thuộc về cả hai."),
        ("apx-m9-super", "super and the abstract pattern", "super is one-level lookup; the abstract-parent-with-collection is the decade's most reused FRQ2 shape.", "super và mẫu trừu tượng", "super là tra-cứu-một-cấp; lớp-cha-trừu tượng-với-bộ-sưu-tập là hình dạng FRQ2 được tái dùng nhất thập kỷ."),
        ("apx-m9-collections", "Polymorphic collections", "One row per element: reference type, object type, which override runs, contribution — and the cast trap.", "Bộ sưu tập đa hình", "Mỗi phần tử một dòng: kiểu tham chiếu, kiểu đối tượng, bản ghi đè nào chạy, đóng góp — và bẫy ép kiểu."),
    ]),
    ("apx-recursion", "apx_m10", [
        ("apx-m10-tracing", "Unroll and roll back", "Single-branch chains unroll to the base and roll back one value per level; parity-switching branches get annotated.", "Trải ra và cuộn lại", "Chuỗi một-nhánh trải xuống cơ sở và cuộn ngược mỗi tầng một giá trị; nhánh đổi-theo-tính-chẵn-lẻ được chú thích."),
        ("apx-m10-bases", "Base cases are the whole grade", "The hunting checklist: what cannot decompose, is there more than one base, does every branch shrink?", "Trường hợp cơ sở là toàn bộ điểm", "Danh sách săn tìm: cái gì không thể phân rã, có nhiều hơn một cơ sở không, mọi nhánh có thu nhỏ không?"),
        ("apx-m10-strings", "Recursive strings and shapes", "Reverse append order, two-index palindromes, Fibonacci-shaped counting, and Euclid's progress-by-modulo.", "Chuỗi đệ quy và các hình dạng", "Thứ tự nối khi đảo ngược, palindrome hai-chỉ-số, đếm hình-Fibonacci, và tiến-triển-theo-modulo của Euclid."),
    ]),
    ("apx-integrated", "apx_m11", [
        ("apx-m11-identify", "Identify before you code", "Underline the nouns and verbs, then name the shape: remove-scan, accumulator, two-pass — shapes transfer, stories don't.", "Nhận diện trước khi viết mã", "Gạch chân danh từ và động từ, rồi gọi tên hình dạng: quét-xóa, bộ tích lũy, hai lượt — hình dạng chuyển giao được, câu chuyện thì không."),
        ("apx-m11-fusion", "Fusion mechanisms", "String scan plus char arithmetic, list-of-arrays with per-row resets, log processing with a surviving accumulator.", "Các cơ chế hợp nhất", "Quét chuỗi cộng phép toán ký tự, danh-sách-mảng với reset từng hàng, xử lý log với bộ tích lũy sống sót."),
        ("apx-m11-plan", "Planning under exam conditions", "Signature first, states listed, boundaries marked, control skeleton in comments — then fill the code.", "Lập kế hoạch trong phòng thi", "Chữ ký trước, liệt kê trạng thái, đánh dấu biên, khung điều khiển dạng chú thích — rồi điền mã."),
    ]),
    ("apx-frq-workshop", "apx_m12", [
        ("apx-m12-anatomy", "Anatomy of an FRQ", "A story, a data table, four tasks: read once for setting, twice for data, write signatures first.", "Giải phẫu một FRQ", "Một câu chuyện, một bảng dữ liệu, bốn nhiệm vụ: đọc một lần cho bối cảnh, hai lần cho dữ liệu, viết chữ ký trước."),
        ("apx-m12-independent", "Parts are independent", "Part (b) never needs part (a); graders score each separately — a botched part must not cascade.", "Các phần độc lập", "Phần (b) không bao giờ cần phần (a); người chấm chấm từng phần riêng — phần hỏng không được lan truyền."),
        ("apx-m12-review", "The five-point self-review", "Signature fidelity, boundary sweep, spec-sentence audit, name honesty, dead-code removal.", "Tự review năm điểm", "Trung thành chữ ký, quét biên, kiểm-toán-câu-đặc-tả, trung thực tên biến, xóa mã chết."),
    ]),
    ("apx-frq-method", "apx_m13", [
        ("apx-m13-spec", "The clause that decides", "Tie-breaks, strictness, sentinels, format rules — circle every operator-deciding word; the circles are the rubric.", "Mệnh đề quyết định", "Phá hòa, nghiêm ngặt, sentinel, luật định dạng — khoanh mọi từ quyết định toán tử; các vòng tròn là bảng điểm."),
        ("apx-m13-edge", "Edge cases by type", "Each data type owns a canonical edge set: run the empty and single-element cases before the example.", "Biên theo kiểu dữ liệu", "Mỗi kiểu dữ liệu sở hữu bộ biên kinh điển: chạy trường hợp rỗng và một-phần-tử trước ví dụ."),
        ("apx-m13-mixed", "From spec to skeleton", "Two passes make tie-breaks one comparison; write the base case and progress first for recursion.", "Từ đặc tả đến khung", "Hai lượt biến phá hòa thành một phép so sánh; với đệ quy viết cơ sở và tiến triển trước."),
    ]),
    ("apx-frq-class", "apx_m14", [
        ("apx-m14-lifecycle", "Lifecycle rules are the problem", "Coins reset on empty; likes at exactly five; both mutators guard the same condition — underline every rule sentence.", "Luật vòng đời là bài toán", "Xu về 0 khi rút trống; được-thích đúng ở lượt năm; cả hai bộ biến đổi chặn cùng điều kiện — gạch chân mọi câu luật."),
        ("apx-m14-interaction", "Holders and delegation", "The truth lives in held objects; the holder asks, never copies — duplicating state drifts.", "Vật chứa và ủy quyền", "Sự thật nằm trong các đối tượng được giữ; vật chứa hỏi, không bao giờ sao chép — nhân bản trạng thái thì lệch."),
        ("apx-m14-rubric", "Reading the rubric into code", "Five rows: fields, constructor, transitions, accessors, no extra API — and the two-minute rule audit that finds missing guards.", "Đọc bảng điểm vào mã", "Năm hàng: trường, constructor, bước chuyển, accessor, không API thừa — và phép kiểm-toán-hai-phút tìm biến chặn thiếu."),
    ]),
    ("apx-frq-debug", "apx_m15", [
        ("apx-m15-diagnose", "A diff against intention", "Spec first, code second: the bug is always 'code does X, spec says Y' — trace the cheapest failing case.", "So khớp với ý định", "Đặc tả trước, mã sau: lỗi luôn là 'mã làm X, đặc tả nói Y' — truy vết trường hợp hỏng rẻ nhất."),
        ("apx-m15-fix", "Fix the cause, not the symptom", "One token usually; re-run the WHOLE test set; say the one-sentence correction before typing.", "Sửa nguyên nhân, không phải triệu chứng", "Thường chỉ một ký tự; chạy lại TOÀN BỘ bộ test; nêu câu sửa một câu trước khi gõ."),
        ("apx-m15-regress", "Regression thinking", "Ask what OTHER inputs the same bug class corrupts — one bug becomes a family inspection.", "Tư duy hồi quy", "Hỏi đầu vào NÀO KHÁC cùng lớp lỗi sẽ bị làm hỏng — một lỗi thành một lần soát cả họ."),
    ]),
    ("apx-partial", "apx_m16", [
        ("apx-m16-parts", "Parts are scored independently", "Inventory parts by type, write recognizable patterns first, budget eight minutes before banking and moving.", "Các phần được chấm độc lập", "Kiểm kê phần theo loại, viết mẫu quen thuộc trước, ngân sách tám phút trước khi giữ và đi tiếp."),
        ("apx-m16-cascade", "Cascades are self-inflicted", "Prefer self-contained implementations; guard boundaries between parts as if they cannot see each other's bugs.", "Lan truyền là tự gây ra", "Ưu tiên cài đặt tự chứa; chặn biên giữa các phần như thể chúng không thấy lỗi của nhau."),
        ("apx-m16-banking", "The three bankable cores", "The count, the existence check, the first-match-with-sentinel — implement, verify, and leave alone.", "Ba lõi dễ giữ", "Phép đếm, kiểm tra tồn tại, khớp-đầu-tiên-với-sentinel — cài, kiểm chứng, và không đụng nữa."),
    ]),
    ("apx-mixed", "apx_m17", [
        ("apx-m17-blend", "The skill of not knowing", "Classify in five seconds (predict / write / fix), name the mechanism, answer in the required mode.", "Kỹ năng không-biết", "Phân loại trong năm giây (dự-đoán / viết / sửa), gọi tên cơ chế, trả lời đúng chế độ yêu cầu."),
        ("apx-m17-shift", "Interleaving works", "Switching mechanisms forces retrieval practice; tally mistakes by mechanism, not topic.", "Xen kẽ có tác dụng", "Đổi cơ chế ép luyện-truy-hồi; đếm lỗi theo cơ chế, không phải chủ đề."),
        ("apx-m17-review", "The cross-module review loop", "Sort misses by the module that taught the mechanism; re-run that practice within 48 hours.", "Vòng ôn liên module", "Xếp câu sai theo module đã dạy cơ chế; chạy lại bộ luyện đó trong 48 giờ."),
    ]),
    ("apx-timed", "apx_m18", [
        ("apx-m18-budget", "The budget is the exercise", "Target times per task type; log target, actual, and the phase that ate the surplus.", "Ngân sách là bài tập", "Thời gian mục tiêu theo loại bài; ghi mục tiêu, thực tế, và giai đoạn ăn phần thừa."),
        ("apx-m18-bottleneck", "Bottleneck autopsies", "Reading, planning, coding, testing fail differently — and most students misdiagnose 'coding' for 'reading'.", "Giải phẫu điểm nghẽn", "Đọc, lập kế hoạch, viết, kiểm thử hỏng khác nhau — và đa số sinh viên chẩn đoán nhầm 'viết' thành 'đọc'."),
        ("apx-m18-retry", "The structured retry", "One change per retry: pre-underlined spec, skeleton only, typing from memory, or boundaries first.", "Lần thử lại có cấu trúc", "Mỗi lần thử lại một thay đổi: đặc tả gạch-sẵn, chỉ khung, gõ từ trí nhớ, hoặc biên trước."),
    ]),
    ("apx-errors", "apx_m19", [
        ("apx-m19-taxonomy", "The thirteen error classes", "Off-by-one to missing-edge: each class has a signature symptom — learn the mapping, debugging becomes lookup.", "Mười ba lớp lỗi", "Từ lệch-một đến thiếu-biên: mỗi lớp có triệu chứng đặc trưng — học bảng ánh xạ, gỡ lỗi thành tra bảng."),
        ("apx-m19-diagnose", "Diagnose before you read the fix", "Compile or runtime? Always wrong or boundary-wrong? Construct the minimal failing input.", "Chẩn đoán trước khi đọc bản sửa", "Lúc biên dịch hay lúc chạy? Luôn sai hay sai-ở-biên? Dựng đầu vào hỏng tối thiểu."),
        ("apx-m19-family", "Family inspection", "Repair the whole family of inputs the bug class corrupts — and calibration matters: not every weird line is a bug.", "Soi cả họ lỗi", "Sửa cả họ đầu vào mà lớp lỗi làm hỏng — và hiệu chuẩn quan trọng: dòng nào trông lạ cũng không phải lỗi."),
    ]),
    ("apx-strategy", "apx_m20", [
        ("apx-m20-pacing", "Pacing both sections", "Two-pass MCQ pacing with slack; the FRQ rhythm of 20 minutes each plus a review bank.", "Nhịp độ cả hai phần", "Nhịp hai lượt cho trắc nghiệm có dự phòng; nhịp FRQ 20 phút mỗi câu cộng quỹ soát."),
        ("apx-m20-triage", "Triage in three bins", "Answer now, return later, eliminate-and-guess — and bin decisions are final for the pass.", "Phân loại ba thùng", "Trả lời ngay, quay lại sau, loại-rồi-đoán — và quyết định thùng chốt cho cả lượt."),
        ("apx-m20-final10", "The last ten minutes", "A protocol: fill blanks, audit boundaries, check signatures, stop rewriting.", "Mười phút cuối", "Một quy trình: điền chỗ trống, kiểm toán biên, kiểm chữ ký, ngừng viết lại."),
    ]),
    ("apx-exam1", "apx_m21", [
        ("apx-m21-rules", "Exam #1 rules of engagement", "Real clock, no notes, answer everything — and the debrief is half the exam.", "Luật tham chiến Đề #1", "Đồng hồ thật, không tài liệu, trả lời mọi câu — và tranh luận là một nửa kỳ thi."),
        ("apx-m21-analysis", "The three-axis scorecard", "Accuracy per mechanism, time-per-item variance, and the two-question redo rule.", "Bảng điểm ba trục", "Độ chính xác theo cơ chế, phương sai thời-gian-mỗi-câu, và luật làm-lại-hai-câu."),
        ("apx-m21-debrief", "Reading difficulty honestly", "This simulation runs above the real median on purpose; fix strategy toward consistency, not the hard tail.", "Đọc độ khó trung thực", "Mô phỏng này cố ý trên mức trung vị thật; sửa chiến lược hướng sự ổn định, không phải phần đuôi khó."),
    ]),
    ("apx-exam2", "apx_m22", [
        ("apx-m22-rules", "Exam #2: the traps change", "Dead variables, near-miss clauses, order assumptions, mirror misapplications — same topics, subtler failures.", "Đề #2: các bẫy đổi", "Biến chết, mệnh đề suýt-khớp, giả định thứ tự, áp-dụng-đối-xứng-sai — cùng chủ đề, thất bại tinh vi hơn."),
        ("apx-m22-analysis", "The trap map", "Four traps, four cures — 'tried hard' is not a diagnosis; 'I assumed mutations commute' is.", "Bản đồ bẫy", "Bốn bẫy, bốn thuốc chữa — 'đã cố hết sức' không phải chẩn đoán; 'tôi đã giả định các phép biến đổi hoán đổi được' mới là."),
        ("apx-m22-trapmap", "Reading the trend line", "Compare accuracy, median time, and trap diversity across simulations — accuracy up because time collapsed means skipped verification.", "Đọc đường xu hướng", "So độ chính xác, thời gian trung vị, và độ đa dạng bẫy giữa các mô phỏng — chính xác tăng vì thời gian sụp có nghĩa là bỏ kiểm chứng."),
    ]),
    ("apx-exam3", "apx_m23", [
        ("apx-m23-rules", "Exam #3: synthesis", "Items fuse two mechanisms where earlier exams fused one mechanism with a trap — find the minute-solvers in the first pass.", "Đề #3: tổng hợp", "Các câu trộn hai cơ chế ở nơi các đề trước trộn một cơ chế với một bẫy — tìm các-câu-giải-được-trong-một-phút ở lượt đầu."),
        ("apx-m23-synthesis", "Decomposing fused items", "Name the data journey, locate the interaction, implement segment-by-segment with one-element tests.", "Phân rã câu hợp nhất", "Gọi tên hành-trình-dữ-liệu, định vị tương tác, cài từng đoạn với kiểm nghiệm một-phần-tử."),
        ("apx-m23-compare", "The pre-master verdict", "Three simulations scored: rising accuracy is readiness; flat-below means one mechanism before the master.", "Phán quyết tiền-thạc-sĩ", "Ba mô phỏng đã chấm: độ chính xác đi lên là sẵn sàng; phẳng-dưới nghĩa là một cơ chế trước thạc sĩ."),
    ]),
    ("apx-master", "apx_m24", [
        ("apx-m24-protocol", "The master protocol", "Timed MCQ half then timed FRQ, no returns mid-set, banking discipline inside the FRQ.", "Quy trình thạc sĩ", "Nửa trắc nghiệm có giờ rồi FRQ có giờ, không quay lại giữa bộ, kỷ luật giữ-điểm trong FRQ."),
        ("apx-m24-verdict", "The verdict rubric", "85% and in-budget is ready; 70–85% is one more cycle; below 70% is routing, not judgment.", "Bảng phán quyết", "85% và trong ngân sách là sẵn sàng; 70–85% là một chu kỳ nữa; dưới 70% là định tuyến, không phải phán xét."),
        ("apx-m24-after", "The week before", "One mixed set, the circling ritual, the strategy re-read, sleep — no new material.", "Tuần trước kỳ thi", "Một bộ hỗn hợp, nghi thức khoanh-tròn, đọc lại chiến lược, ngủ — không tài liệu mới."),
    ]),
]

for mod, script, lessons in PLAN:
    m = importlib.import_module(script)  # runs the (idempotent) module writes
    L = [m.L1, m.L2, m.L3]
    VI = [m.VI_L1, m.VI_L2, m.VI_L3]
    for i, (lid, title, desc, vi_title, vi_desc) in enumerate(lessons):
        # checkpoints are authored by the module scripts themselves; this
        # writes the three teaching lessons around the existing bodies.
        apx.write_lesson(mod, lid, title, desc, 10, L[i], vi_title, vi_desc, VI[i])

print("teaching lessons written")
