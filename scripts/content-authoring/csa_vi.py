"""VI overlays for C# Advanced challenges: {cid: {"title","prompt","hints"}}."""

VI: dict[str, dict] = {
    "csa-checkpoint-m1-task": {
        "title": "Checkpoint ngữ nghĩa ngôn ngữ",
        "prompt": (
            "Hiện thực `static string Classify(int input)` trong lớp `Solution`. Quy tắc: "
            "trả về \"default\" cho 0, \"negative\" khi dưới 0, \"small\" cho 1–99, còn lại \"large\". "
            "Sau đó trả lời các câu hỏi về hành vi boxing trong test thứ hai bằng giá trị chính xác được yêu cầu."
        ),
        "hints": {
            "classification": "Bốn khoảng theo thứ tự: âm, 0, 1–99, 100+.",
            "boxing-truth": "Unbox sao chép giá trị; Equals trên value type đã box so giá trị; các box là object khác nhau.",
        },
    },
    "csa-p1-copy-vs-ref": {
        "title": "Bản sao so với tham chiếu",
        "prompt": (
            "Hiện thực `static (int, int) Twist()`: tạo một struct điểm (3,4), gán cho biến thứ hai, "
            "sửa biến thứ hai thành (10,20), và trả về tọa độ của điểm ĐẦU TIÊN. Struct sao chép khi gán — "
            "điểm đầu tiên phải nguyên vẹn."
        ),
        "hints": {
            "struct-copy": "Sửa bản sao không được ảnh hưởng bản gốc — trả về trường của bản gốc.",
        },
    },
    "csa-p1-box-counter": {
        "title": "Đếm các box",
        "prompt": (
            "Hiện thực `static int Sum(ReadOnlySpan<int> values)` cộng một span KHÔNG boxing, và "
            "`static object BoxSum(ReadOnlySpan<int> values)` trả về tổng dưới dạng object (phép này box "
            "đúng một lần, ở lệnh return). Test kiểm tra cả giá trị lẫn việc BoxSum trả về một int đã box."
        ),
        "hints": {
            "sum-unboxed": "Duyệt span không cấp phát gì — chỉ cần cộng dồn.",
            "box-once": "Trả về tổng đã chuyển sang object — một box ở ranh giới.",
        },
    },
    "csa-p1-null-gate": {
        "title": "Cổng null-state",
        "prompt": (
            "Hiện thực `static int LengthOrMinus(string? text)`: trả về -1 khi text null, ngược lại trả "
            "Length. Rồi hiện thực `static string Coalesce(string? a, string? b)`: giá trị đầu tiên khác "
            "null trong a và b, hoặc \"<empty>\". Test bám sát hợp đồng null-state với nullable reference types."
        ),
        "hints": {
            "length-or-minus": "So khớp null trước, sau đó Length an toàn.",
            "coalesce-chain": "Chuỗi ?? chạy trái sang phải; một fallback hằng cho trường hợp đều null.",
        },
    },
    "csa-p1-resolution-prediction": {
        "title": "Dự đoán resolution",
        "prompt": (
            "Cặp overload dạy luật betterness. Hiện thực lớp `Solution` với `static string Pick(int v)` "
            "trả về \"int\", `static string Pick(long v)` trả về \"long\", `static string Pick(object v)` "
            "trả về \"object\", và `static string Pick<T>(T v)` trả về \"generic\". Thứ tự overload trong "
            "định nghĩa KHÔNG quyết định lựa chọn — luật tốt hơn của compiler quyết định; test gọi với "
            "literal nhiều kiểu khác nhau."
        ),
        "hints": {
            "literal-types": "Kiểu khớp chính xác thắng generic; T cố định tại call site thắng object.",
        },
    },
}
