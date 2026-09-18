#!/usr/bin/env python3
"""C — Intermediate — Module 12: cint-files.

Files as bytes: text vs binary mode, fwrite/fread records, endianness as
a real cost, random access with fseek/ftell, and the robust-reader
pattern (magic, version, checksum) that survives bad input. Graded
against /tmp files — verified in the sandbox probe. House conventions.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cint import (
    write_module, write_lesson, write_practice, challenge, vi_challenge,
    write_checkpoint, C_PRELUDE,
)

M = "cint-files"

write_module(
    M,
    "Binary Files & Robust Parsing",
    "Records on disk: magic numbers, endianness, checksums, random access — "
    "and reading files you do not trust.",
    "Tệp nhị phân & parsing bền vững",
    "Record trên đĩa: magic number, endianness, checksum, truy cập ngẫu "
    "nhiên — và đọc tệp bạn không tin tưởng.",
    lessons=["bytes-on-disk", "random-access", "robust-reader", "cint-checkpoint-m12"],
    practices=["cint-p12-records", "cint-p12-parser"],
)

# ---------------------------------------------------------------- lessons

write_lesson(
    M, "bytes-on-disk",
    "Records as Bytes",
    "fwrite/fread move bytes, not fields. Struct layout, endianness, and "
    "the record header that makes files self-describing.",
    17,
    r"""
## fwrite moves bytes — including padding

```c
struct Rec { long id; int qty; };
struct Rec r = {7, 3};
fwrite(&r, sizeof r, 1, f);   /* writes 16 bytes on a 64-bit libc:
                                 8 (id) + 4 (qty) + 4 (padding!) */
```

The four padding bytes are *garbage carried to disk* — worse, they are
non-portable: a different compiler or ABI lays the struct out
differently and your file format breaks. Portable record I/O writes
**fields, not structs**:

```c
/* field-by-field, fixed widths, defined by YOU */
uint32_t id = (uint32_t)r.id;
fwrite(&id, sizeof id, 1, f);
```

## Endianness is a tax you pay once

Little-endian machines store the low byte first. If a file is written
as raw `uint32_t`, an x86 writer and a big-endian reader disagree on
every multi-byte field. Formats that live beyond one machine define a
byte order (network order = big-endian) and convert at the boundary:

```c
/* little-endian write of a 32-bit value, byte by byte */
unsigned char b[4] = { v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF, (v >> 24) & 0xFF };
fwrite(b, 4, 1, f);
```

Byte-by-byte I/O is slower but *defines* the format — no platform can
disagree with you about it.

## The self-describing header

Every non-trivial binary format starts with a header: magic number
(your format's signature), version, count. Readers check all three
*before* trusting anything else:

```c
unsigned char hdr[8];
fread(hdr, 1, 8, f) == 8 || die();
memcmp(hdr, "CJR1", 4) == 0 || die("wrong magic");
/* hdr[4..7] = record count, little-endian */
```

`fread` returning fewer bytes than asked is the *normal* failure mode
of short files — not an exotic event. Counting your bytes is the
discipline.
""",
"Record như byte",
    "fwrite/fread chuyển byte, không phải trường. Layout struct, "
    "endianness, và record header khiến tệp tự mô tả.",
    r"""
## fwrite chuyển byte — kể cả padding

```c
struct Rec { long id; int qty; };
struct Rec r = {7, 3};
fwrite(&r, sizeof r, 1, f);   /* ghi 16 byte trên libc 64-bit:
                                 8 (id) + 4 (qty) + 4 (padding!) */
```

Bốn byte padding là *rác mang lên đĩa* — tệ hơn, chúng không portable:
compiler hoặc ABI khác bố trí struct khác đi và định dạng tệp của bạn
gãy. Record I/O portable ghi **từng trường, không phải struct**:

```c
/* từng trường, độ rộng cố định, do BẠN định nghĩa */
uint32_t id = (uint32_t)r.id;
fwrite(&id, sizeof id, 1, f);
```

## Endianness là loại thuế trả một lần

Máy little-endian lưu byte thấp trước. Nếu tệp ghi `uint32_t` thô, máy
viết x86 và máy đọc big-endian bất đồng ở mọi trường nhiều byte. Định
dạng sống qua nhiều máy định nghĩa thứ tự byte (network order =
big-endian) và đổi tại biên giới:

```c
/* ghi 32-bit little-endian, từng byte */
unsigned char b[4] = { v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF, (v >> 24) & 0xFF };
fwrite(b, 4, 1, f);
```

I/O từng byte chậm hơn nhưng *định nghĩa* định dạng — không platform nào
bất đồng với bạn về nó.

## Header tự mô tả

Mọi định dạng nhị phân không tầm thường mở đầu bằng header: magic number
(chữ ký định dạng), version, count. Reader kiểm cả ba *trước khi* tin
bất cứ gì khác:

```c
unsigned char hdr[8];
fread(hdr, 1, 8, f) == 8 || die();
memcmp(hdr, "CJR1", 4) == 0 || die("wrong magic");
/* hdr[4..7] = số record, little-endian */
```

`fread` trả ít byte hơn yêu cầu là *chế độ thất bại bình thường* của tệp
ngắn — không phải sự kiện lạ. Đếm byte của bạn là kỷ luật.
"""
)

write_lesson(
    M, "random-access",
    "Random Access & Positions",
    "fseek/ftell turn a file into an array: fixed-width records, O(1) "
    "seeks, and the update-in-place trap.",
    16,
    r"""
## A file is an array you can index

Fixed-width records make any record reachable directly:

```c
/* record i of width W: */
fseek(f, (long)i * W, SEEK_SET);   /* SEEK_SET: from the start */
fread(buf, W, 1, f);
```

`ftell` reports the current position; `SEEK_CUR` moves relative, and
`SEEK_END` from the tail (`fseek(f, 0, SEEK_END); ftell(f)` is the
classical file-size idiom — though for real sizes, prefer the OS stat
API; this is the stdlib-only version).

## "r+" is read AND write — not append

Opening with `"r+"` allows both directions but does **not** create the
file and does **not** move the position for you: after writing, the
position is where you stopped. `"a"` (append) always writes at the end
but reads nowhere. Modes are contracts — table them once:

| mode | reads | writes | creates | truncates |
|---|---|---|---|---|
| "r" | ✓ | ✗ | ✗ | ✗ |
| "w" | ✗* | ✓ | ✓ | ✓ |
| "a" | ✗ | ✓ | ✓ | ✗ |
| "r+" | ✓ | ✓ | ✗ | ✗ |
| "w+" | ✓* | ✓ | ✓ | ✓ |

\* only after rewinding; "w" truncates on open, destroying existing data —
the mode that deletes files when chosen carelessly.

## Update in place: the width must match

Overwriting record i via `"r+"` works only if the new record has
*exactly* the same width — otherwise everything after it shifts and the
file is corrupt. Variable-width updates rewrite the tail or use an
indirection (slot table) — the reason real databases are complicated.
""",
"Truy cập ngẫu nhiên & vị trí",
    "fseek/ftell biến tệp thành mảng: record độ rộng cố định, seek O(1), "
    "và bẫy update-tại-chỗ.",
    r"""
## Tệp là mảng bạn đánh chỉ số được

Record độ rộng cố định cho phép tới bất kỳ record nào trực tiếp:

```c
/* record i có độ rộng W: */
fseek(f, (long)i * W, SEEK_SET);   /* SEEK_SET: từ đầu */
fread(buf, W, 1, f);
```

`ftell` báo vị trí hiện tại; `SEEK_CUR` di chuyển tương đối, và
`SEEK_END` từ đuôi (`fseek(f, 0, SEEK_END); ftell(f)` là cách kinh điển
lấy kích thước tệp — với kích thước thật, dùng stat API của OS; đây là
bản stdlib-only).

## "r+" là đọc VÀ ghi — không phải append

Mở bằng `"r+"` cho phép cả hai hướng nhưng **không** tạo tệp và
**không** tự dời vị trí: sau khi ghi, vị trí nằm nơi bạn dừng. `"a"`
(append) luôn ghi ở cuối nhưng không đọc được. Mode là hợp đồng — lập
bảng một lần:

| mode | đọc | ghi | tạo | cắt cụt |
|---|---|---|---|---|
| "r" | ✓ | ✗ | ✗ | ✗ |
| "w" | ✗* | ✓ | ✓ | ✓ |
| "a" | ✗ | ✓ | ✓ | ✗ |
| "r+" | ✓ | ✓ | ✗ | ✗ |
| "w+" | ✓* | ✓ | ✓ | ✓ |

\* chỉ sau khi rewind; "w" cắt cụt khi mở, phá dữ liệu cũ — mode xóa tệp
khi chọn ẩu.

## Update tại chỗ: độ rộng phải khớp

Ghi đè record i qua `"r+"` chỉ đúng khi record mới có *đúng* độ rộng cũ
— không thì mọi thứ phía sau dịch chuyển và tệp hỏng. Update độ rộng
thay đổi phải viết lại phần đuôi hoặc dùng gián tiếp (slot table) — lý
do database thật phức tạp.
"""
)

write_lesson(
    M, "robust-reader",
    "The Robust Reader",
    "Checksums, bounds, and failure as a first-class return value: reading "
    "files that may be truncated, corrupted, or hostile.",
    17,
    r"""
## Assume the file is lying

A robust reader treats every byte as suspect:

1. **Check every read's return count.** `fread` returns items read;
   short reads mean truncation.
2. **Validate before use.** Magic, version, record counts, field
   ranges — reject anything outside the format you defined.
3. **Checksum the payload.** A checksum cannot prove integrity, but it
   catches the corruption that actually happens (torn writes, bit rot,
   truncated transfers).

```c
/* FNV-1a over a file's bytes */
unsigned long file_checksum(FILE *f, long size) {
    unsigned long h = 2166136261UL;
    int c;
    while (size-- > 0 && (c = fgetc(f)) != EOF)
        h = (h ^ (unsigned long)c) * 16777619UL;
    return h;
}
```

Store the checksum *with* the data (header or trailer); the reader
recomputes and compares. Mismatch = reject the file, don't guess.

## Failure is a return value

C's file functions signal through return codes — `NULL` from fopen,
item-count from fread, `EOF` from fgetc. The robust shape is one error
path:

```c
int load(const char *path, Doc *out) {
    FILE *f = fopen(path, "rb");
    if (!f) return -1;                       /* errno says why */
    /* ... every step checks and bails ... */
    fclose(f);
    return 0;
}
```

`fclose` on the success path *and* every bail path — the leak in file
form. (The pattern that finally mechanizes this discipline, RAII /
`__attribute__((cleanup))`, is outside ISO C; the honest habit is a
single `goto cleanup` exit or scrupulous pairing.)
""",
"Reader bền vững",
    "Checksum, biên, và thất bại như giá trị trả về hạng nhất: đọc các "
    "tệp có thể bị cắt, hỏng, hoặc thù địch.",
    r"""
## Coi tệp đang nói dối

Reader bền vững coi mọi byte là đáng ngờ:

1. **Kiểm return count của mọi lần đọc.** `fread` trả số item đọc được;
   đọc ngắn nghĩa là cắt cụt.
2. **Kiểm trước khi dùng.** Magic, version, số record, khoảng giá trị
   trường — từ chối mọi thứ ngoài định dạng bạn định nghĩa.
3. **Checksum payload.** Checksum không chứng minh toàn vẹn, nhưng bắt
   được hư hỏng thật sự (ghi đứt, bit rot, truyền bị cắt).

```c
/* FNV-1a trên các byte của tệp */
unsigned long file_checksum(FILE *f, long size) {
    unsigned long h = 2166136261UL;
    int c;
    while (size-- > 0 && (c = fgetc(f)) != EOF)
        h = (h ^ (unsigned long)c) * 16777619UL;
    return h;
}
```

Lưu checksum *cùng* dữ liệu (header hoặc trailer); reader tính lại và so
sánh. Lệch = từ chối tệp, không đoán.

## Thất bại là giá trị trả về

Các hàm tệp của C báo hiệu qua return code — `NULL` từ fopen, số item từ
fread, `EOF` từ fgetc. Dạng bền vững là một đường lỗi duy nhất:

```c
int load(const char *path, Doc *out) {
    FILE *f = fopen(path, "rb");
    if (!f) return -1;                       /* errno nói lý do */
    /* ... mọi bước kiểm và thoát ... */
    fclose(f);
    return 0;
}
```

`fclose` trên đường thành công *và* mọi đường thoát giữa chừng — leak ở
dạng tệp. (Mẫu cơ giới hóa kỷ luật này, RAII /
`__attribute__((cleanup))`, nằm ngoài ISO C; thói quen trung thực là một
lối `goto cleanup` hoặc ghép cặp cẩn trọng.)
"""
)

# ---------------------------------------------------------------- practice

write_practice(
    M, "cint-p12-records",
    "Record I/O Gym",
    "Field-wise binary records with a magic header — write, verify, re-read.",
    "Phòng gym record I/O",
    "Record nhị phân từng trường với magic header — ghi, kiểm, đọc lại.",
    after_lesson="random-access",
    minutes=28,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p12-csv-record",
            "The Fixed-Width Record Store",
            """Implement a tiny record store over `/tmp/cj_records.bin`.
The boilerplate declares:

```c
/* file format:
   bytes 0..3  : magic "CJR1"
   bytes 4..5  : uint16 record count (little-endian)
   then records of exactly 8 bytes each:
     byte 0    : id (0..255)
     bytes 1..4: int32 qty little-endian
     bytes 5..7: zero padding
*/
int rs_create(const char *path);                    /* fresh empty store */
int rs_append(const char *path, unsigned id, int qty); /* 0 ok, -1 err/bad args */
int rs_read(const char *path, size_t index,
            unsigned *id, int *qty);                /* 0 ok, -1 out of range/err */
size_t rs_count(const char *path);                  /* 0 if absent/invalid */
```

All multi-byte fields little-endian, byte by byte (endianness tax).""",
            C_PRELUDE + "\n#include <stdio.h>\n#include <stddef.h>\n#include <stdint.h>\nint rs_create(const char *path);\nint rs_append(const char *path, unsigned id, int qty);\nint rs_read(const char *path, size_t index, unsigned *id, int *qty);\nsize_t rs_count(const char *path);\n",
            [
                (
                    "write then re-read",
                    r"""
const char *p = "/tmp/cj_records.bin";
CHECK_EQ(rs_create(p), 0);
CHECK_EQ(rs_count(p), 0u);
CHECK_EQ(rs_read(p, 0, NULL, NULL), -1);          /* empty */
CHECK_EQ(rs_append(p, 1, 100), 0);
CHECK_EQ(rs_append(p, 2, 200), 0);
CHECK_EQ(rs_append(p, 3, 300), 0);
CHECK_EQ(rs_count(p), 3u);
unsigned id; int qty;
CHECK_EQ(rs_read(p, 0, &id, &qty), 0);
CHECK(id == 1 && qty == 100);
CHECK_EQ(rs_read(p, 2, &id, &qty), 0);
CHECK(id == 3 && qty == 300);
CHECK_EQ(rs_read(p, 3, &id, &qty), -1);           /* past the end */
CHECK_EQ(rs_append(p, 300, 1), -1);               /* id must fit a byte */
CHECK_EQ(rs_count(p), 3u);                        /* unchanged */
""",
                    "Append: fseek to header, read count, fseek past last record, write 8 bytes, rewrite count. Count: read bytes 4..5.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p12-csv-record": vi_challenge(
            "Kho record cố định",
            "Cài rs_create/append/read/count cho định dạng 8-byte/record, little-endian, magic CJR1.",
            [("ghi rồi đọc lại", "append: đọc count, seek qua cuối, ghi 8 byte, viết lại count.")],
        ),
    },
    solutions=[
        (
            "cint-p12-csv-record",
            r"""
#include <string.h>
#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
static void put_u16le(unsigned char *b, unsigned v) {
    b[0] = v & 0xFF; b[1] = (v >> 8) & 0xFF;
}
static void put_i32le(unsigned char *b, long v) {
    b[0] = v & 0xFF; b[1] = (v >> 8) & 0xFF;
    b[2] = (v >> 16) & 0xFF; b[3] = (v >> 24) & 0xFF;
}
static unsigned get_u16le(const unsigned char *b) {
    return b[0] | ((unsigned)b[1] << 8);
}
static long get_i32le(const unsigned char *b) {
    return (long)b[0] | ((long)b[1] << 8) | ((long)b[2] << 16) | ((long)b[3] << 24);
}
static size_t read_count(FILE *f) {
    unsigned char b[2];
    if (fseek(f, 4, SEEK_SET) != 0) return 0;
    if (fread(b, 1, 2, f) != 2) return 0;
    return get_u16le(b);
}
int rs_create(const char *path) {
    if (!path) return -1;
    FILE *f = fopen(path, "wb");
    if (!f) return -1;
    unsigned char hdr[6] = { 'C', 'J', 'R', '1', 0, 0 };
    int ok = fwrite(hdr, 1, 6, f) == 6;
    fclose(f);
    return ok ? 0 : -1;
}
int rs_append(const char *path, unsigned id, int qty) {
    if (!path || id > 255) return -1;
    FILE *f = fopen(path, "r+b");
    if (!f) return -1;
    size_t n = read_count(f);
    unsigned char rec[8] = {0};
    rec[0] = (unsigned char)id;
    put_i32le(&rec[1], qty);
    int ok = fseek(f, (long)(6 + n * 8), SEEK_SET) == 0
          && fwrite(rec, 1, 8, f) == 8;
    if (ok) {
        unsigned char cb[2];
        put_u16le(cb, (unsigned)(n + 1));
        ok = fseek(f, 4, SEEK_SET) == 0 && fwrite(cb, 1, 2, f) == 2;
    }
    fclose(f);
    return ok ? 0 : -1;
}
int rs_read(const char *path, size_t index, unsigned *id, int *qty) {
    if (!path) return -1;
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    size_t n = read_count(f);
    if (index >= n) { fclose(f); return -1; }
    unsigned char rec[8];
    int ok = fseek(f, (long)(6 + index * 8), SEEK_SET) == 0
          && fread(rec, 1, 8, f) == 8;
    fclose(f);
    if (!ok) return -1;
    if (id) *id = rec[0];
    if (qty) *qty = (int)get_i32le(&rec[1]);
    return 0;
}
size_t rs_count(const char *path) {
    if (!path) return 0;
    FILE *f = fopen(path, "rb");
    if (!f) return 0;
    unsigned char hdr[4];
    if (fread(hdr, 1, 4, f) != 4 || memcmp(hdr, "CJR1", 4) != 0) {
        fclose(f);
        return 0;
    }
    size_t n = read_count(f);
    fclose(f);
    return n;
}""",
            r"""
#include <string.h>
#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
static void put_u16le(unsigned char *b, unsigned v) {
    b[0] = v & 0xFF; b[1] = (v >> 8) & 0xFF;
}
static void put_i32le(unsigned char *b, long v) {
    b[0] = v & 0xFF; b[1] = (v >> 8) & 0xFF;
    b[2] = (v >> 16) & 0xFF; b[3] = (v >> 24) & 0xFF;
}
static unsigned get_u16le(const unsigned char *b) {
    return b[0] | ((unsigned)b[1] << 8);
}
static long get_i32le(const unsigned char *b) {
    return (long)b[0] | ((long)b[1] << 8) | ((long)b[2] << 16) | ((long)b[3] << 24);
}
int rs_create(const char *path) {
    if (!path) return -1;
    FILE *f = fopen(path, "wb");
    if (!f) return -1;
    unsigned char hdr[6] = { 'C', 'J', 'R', '1', 0, 0 };
    fwrite(hdr, 1, 6, f);
    fclose(f);
    return 0;
}
int rs_append(const char *path, unsigned id, int qty) {
    if (!path) return -1;                     /* wrong: id > 255 accepted */
    FILE *f = fopen(path, "r+b");
    if (!f) return -1;
    fseek(f, 0, SEEK_END);
    unsigned char rec[8] = {0};
    rec[0] = (unsigned char)id;
    put_i32le(&rec[1], qty);
    int ok = fwrite(rec, 1, 8, f) == 8;
    long size = ftell(f);
    unsigned char cb[2];
    put_u16le(cb, (unsigned)((size - 6) / 8));
    fseek(f, 4, SEEK_SET);
    fwrite(cb, 1, 2, f);                      /* right idea, but... */
    fclose(f);
    (void)ok;
    return 0;
}
int rs_read(const char *path, size_t index, unsigned *id, int *qty) {
    if (!path) return -1;
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    fseek(f, (long)(6 + index * 8), SEEK_SET);  /* wrong: no count check —
                                                  index past the end reads
                                                  garbage or "succeeds" at EOF */
    unsigned char rec[8];
    size_t got = fread(rec, 1, 8, f);
    fclose(f);
    if (got != 8) return -1;
    if (id) *id = rec[0];
    if (qty) *qty = (int)get_i32le(&rec[1]);
    return 0;
}
size_t rs_count(const char *path) {
    if (!path) return 0;
    FILE *f = fopen(path, "rb");
    if (!f) return 0;
    fseek(f, 4, SEEK_SET);
    unsigned char b[2];
    fread(b, 1, 2, f);
    fclose(f);
    return get_u16le(b);                      /* wrong: no magic check */
}""",
        ),
    ],
)

write_practice(
    M, "cint-p12-parser",
    "Robust Reader Gym",
    "Checksummed binary blobs that reject corruption, and a log parser that never trusts a line.",
    "Phòng gym reader bền vững",
    "Blob nhị phân có checksum từ chối hư hỏng, và parser log không bao giờ tin một dòng.",
    after_lesson="robust-reader",
    minutes=26,
    difficulty="intermediate",
    challenges=[
        challenge(
            "cint-p12-blob",
            "The Checksummed Blob",
            """Implement blob write/read with integrity checking. The
boilerplate declares:

```c
/* format: 4-byte magic "CJB1" | uint32 len LE | len payload bytes |
           4-byte FNV-1a checksum of the payload, LE */
int blob_write(const char *path, const unsigned char *data, size_t len);
/* reads and verifies: 0 ok (fills *out = malloc'd payload, *len),
   -1 on any error: missing file, bad magic, checksum mismatch,
   allocation failure. Caller frees *out. */
int blob_read(const char *path, unsigned char **out, size_t *len);
```

FNV-1a: h = 2166136261u; per byte: h ^= b; h *= 16777619u.""",
            C_PRELUDE + "\n#include <stdio.h>\n#include <stddef.h>\n#include <stdint.h>\nint blob_write(const char *path, const unsigned char *data, size_t len);\nint blob_read(const char *path, unsigned char **out, size_t *len);\n",
            [
                (
                    "round-trip and corruption rejected",
                    r"""
const char *p = "/tmp/cj_blob.bin";
unsigned char payload[] = {1, 2, 3, 4, 5};
CHECK_EQ(blob_write(p, payload, 5), 0);
unsigned char *got = NULL;
size_t n = 0;
CHECK_EQ(blob_read(p, &got, &n), 0);
CHECK_EQ(n, 5u);
for (int i = 0; i < 5; i++) CHECK_EQ(got[i], payload[i]);
free(got);
CHECK_EQ(blob_write(p, NULL, 3), -1);       /* NULL data */
CHECK_EQ(blob_read("/tmp/cj_absent.bin", &got, &n), -1);
/* corrupt one payload byte */
FILE *f = fopen(p, "r+b");
CHECK(f != NULL);
fseek(f, 8, SEEK_SET);                       /* first payload byte */
fputc(0xEE, f);
fclose(f);
CHECK_EQ(blob_read(p, &got, &n), -1);        /* checksum mismatch */
""",
                    "Write: magic, len, payload, checksum. Read: verify all of it before handing out memory.",
                ),
            ],
        ),
    ],
    vi_challenges={
        "cint-p12-blob": vi_challenge(
            "Blob có checksum",
            "Cài blob_write/blob_read: magic CJB1, len LE, payload, checksum FNV-1a — đọc phải verify mọi thứ.",
            [("round-trip và từ chối hư hỏng", "ghi: magic, len, payload, checksum. đọc: verify trước khi cấp phát.")],
        ),
    },
    solutions=[
        (
            "cint-p12-blob",
            r"""
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
static uint32_t fnv1a(const unsigned char *p, size_t n) {
    uint32_t h = 2166136261u;
    for (size_t i = 0; i < n; i++) {
        h ^= p[i];
        h *= 16777619u;
    }
    return h;
}
static void put_u32le(unsigned char *b, uint32_t v) {
    b[0] = v & 0xFF; b[1] = (v >> 8) & 0xFF;
    b[2] = (v >> 16) & 0xFF; b[3] = (v >> 24) & 0xFF;
}
static uint32_t get_u32le(const unsigned char *b) {
    return (uint32_t)b[0] | ((uint32_t)b[1] << 8)
         | ((uint32_t)b[2] << 16) | ((uint32_t)b[3] << 24);
}
int blob_write(const char *path, const unsigned char *data, size_t len) {
    if (!path || !data) return -1;
    FILE *f = fopen(path, "wb");
    if (!f) return -1;
    unsigned char hdr[8] = { 'C', 'J', 'B', '1', 0, 0, 0, 0 };
    put_u32le(&hdr[4], (uint32_t)len);
    int ok = fwrite(hdr, 1, 8, f) == 8
          && (len == 0 || fwrite(data, 1, len, f) == len);
    if (ok) {
        unsigned char ck[4];
        put_u32le(ck, fnv1a(data, len));
        ok = fwrite(ck, 1, 4, f) == 4;
    }
    fclose(f);
    return ok ? 0 : -1;
}
int blob_read(const char *path, unsigned char **out, size_t *len) {
    if (!path || !out || !len) return -1;
    *out = NULL;
    *len = 0;
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    unsigned char hdr[8];
    if (fread(hdr, 1, 8, f) != 8 || memcmp(hdr, "CJB1", 4) != 0) {
        fclose(f);
        return -1;
    }
    uint32_t n = get_u32le(&hdr[4]);
    unsigned char *buf = malloc(n ? n : 1);
    if (!buf) { fclose(f); return -1; }
    if (fread(buf, 1, n, f) != n) {
        free(buf);
        fclose(f);
        return -1;
    }
    unsigned char ck[4];
    if (fread(ck, 1, 4, f) != 4 || get_u32le(ck) != fnv1a(buf, n)) {
        free(buf);
        fclose(f);
        return -1;
    }
    fclose(f);
    *out = buf;
    *len = n;
    return 0;
}""",
            r"""
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
static uint32_t fnv1a(const unsigned char *p, size_t n) {
    uint32_t h = 2166136261u;
    for (size_t i = 0; i < n; i++) {
        h ^= p[i];
        h *= 16777619u;
    }
    return h;
}
static void put_u32le(unsigned char *b, uint32_t v) {
    b[0] = v & 0xFF; b[1] = (v >> 8) & 0xFF;
    b[2] = (v >> 16) & 0xFF; b[3] = (v >> 24) & 0xFF;
}
static uint32_t get_u32le(const unsigned char *b) {
    return (uint32_t)b[0] | ((uint32_t)b[1] << 8)
         | ((uint32_t)b[2] << 16) | ((uint32_t)b[3] << 24);
}
int blob_write(const char *path, const unsigned char *data, size_t len) {
    if (!path || !data) return -1;
    FILE *f = fopen(path, "wb");
    if (!f) return -1;
    unsigned char hdr[8] = { 'C', 'J', 'B', '1', 0, 0, 0, 0 };
    put_u32le(&hdr[4], (uint32_t)len);
    fwrite(hdr, 1, 8, f);
    fwrite(data, 1, len, f);
    unsigned char ck[4];
    put_u32le(ck, fnv1a(data, len));
    fwrite(ck, 1, 4, f);
    fclose(f);                                 /* wrong: no error checking on
                                                  ANY write — disk-full silently
                                                  produces a truncated file */
    return 0;
}
int blob_read(const char *path, unsigned char **out, size_t *len) {
    if (!path || !out || !len) return -1;
    *out = NULL;
    *len = 0;
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    unsigned char hdr[8];
    fread(hdr, 1, 8, f);                       /* wrong: count unchecked */
    uint32_t n = get_u32le(&hdr[4]);
    unsigned char *buf = malloc(n ? n : 1);
    if (!buf) { fclose(f); return -1; }
    fread(buf, 1, n, f);                       /* wrong: short read not detected */
    fclose(f);
    *out = buf;                                /* wrong: checksum never verified */
    *len = n;
    return 0;
}""",
        ),
    ],
)

# ------------------------------------------------------------- checkpoint

CP_CH = challenge(
    "cint-checkpoint-m12-task",
    "Load a Possibly-Corrupt Database",
    """The checkpoint: a reader for the record store from this module's
first challenge — hardened. The boilerplate declares:

```c
/* same format as rs_*: "CJR1" | u16 count LE | count * 8-byte records
   (id:u8, qty:i32 LE, 3 pad). BUT the file may be truncated, corrupted,
   or missing. The reader must:
   - return -1 for any structural violation (missing/bad magic,
     count beyond file size, short records)
   - return the number of VALID records read into out (capacity cap),
     filling only records whose full 8 bytes exist
   - not allocate, not crash on any input */
long db_load(const char *path, unsigned char *out, size_t cap);
```

out is a flat buffer of cap * 8 bytes; record i lives at out + i*8.""",
    C_PRELUDE + "\n#include <stdio.h>\n#include <stddef.h>\nlong db_load(const char *path, unsigned char *out, size_t cap);\n",
    [
        (
            "never crash, never over-read",
            r"""
/* build a valid 2-record file via the known format */
FILE *f = fopen("/tmp/cj_db.bin", "wb");
CHECK(f != NULL);
unsigned char good[] = {
    'C','J','R','1', 2, 0,
    1, 100,0,0,0, 0,0,0,
    2, 200,0,0,0, 0,0,0,
};
fwrite(good, 1, sizeof good, f);
fclose(f);
unsigned char buf[16];
CHECK_EQ(db_load("/tmp/cj_db.bin", buf, 2), 2);
CHECK_EQ(buf[0], 1);
CHECK_EQ(buf[8], 2);
/* truncated file: header promises 2 records, only 1 present */
f = fopen("/tmp/cj_cut.bin", "wb");
CHECK(f != NULL);
fwrite(good, 1, 6 + 8, f);                    /* header + one record */
fclose(f);
CHECK_EQ(db_load("/tmp/cj_cut.bin", buf, 2), 1);
/* bad magic */
f = fopen("/tmp/cj_bad.bin", "wb");
CHECK(f != NULL);
unsigned char bad[] = { 'X','Y','Z','1', 0, 0 };
fwrite(bad, 1, sizeof bad, f);
fclose(f);
CHECK_EQ(db_load("/tmp/cj_bad.bin", buf, 2), -1);
CHECK_EQ(db_load("/tmp/cj_absent.bin", buf, 2), -1);
CHECK_EQ(db_load(NULL, buf, 2), -1);
CHECK_EQ(db_load("/tmp/cj_db.bin", NULL, 2), -1);
""",
            "Stat-by-read: read the header, then read records one at a time; a short record read stops the scan (count what you got).",
        ),
    ],
)

CP_VI = [
    vi_challenge(
        "Load database có thể hỏng",
        "Cài db_load: kiểm magic, đếm record theo byte thực đọc được, không crash, không over-read.",
        [("không bao giờ crash, không bao giờ đọc quá", "đọc header, rồi từng record; đọc ngắn thì dừng, đếm số nhận được.")],
    ),
]

write_checkpoint(
    M, "cint-checkpoint-m12",
    "Checkpoint: Trust Nothing on Disk",
    "Prove the robust reader: valid data in, garbage rejected, no crash on any input.",
    28,
    r"""
## The task

Implement `db_load` (see the challenge). This is the module's contract
made executable: the happy path is easy, but the graded cases are the
truncated file, the wrong magic, the missing file, and the NULL
arguments. A reader that returns sane errors instead of crashing is the
difference between a tool and a liability.

Passing this proves you can read untrusted bytes the way production
code must: bounds-checked, error-valued, allocation-free.

Next module: return codes, errno, and APIs designed so failure is
impossible to ignore.
""",
    "Kiểm tra: Không tin gì trên đĩa",
    "Chứng minh reader bền vững: dữ liệu hợp lệ vào, rác bị từ chối, không crash với input nào.",
    r"""
## Bài toán

Cài `db_load` (xem challenge). Đây là hợp đồng của module biến thành code
chạy được: đường hạnh phúc dễ, nhưng các trường hợp chấm điểm là tệp bị
cắt, sai magic, tệp mất, và tham số NULL. Reader trả lỗi hợp lý thay vì
crash là ranh giới giữa công cụ và rủi ro.

Vượt qua chứng minh bạn đọc byte không tin tưởng như code production
phải: kiểm biên, trả giá trị lỗi, không cấp phát.

Module sau: return code, errno, và API thiết kế để thất bại không thể
bị bỏ qua.
""",
    CP_CH,
    CP_VI,
    solution=r"""
#include <string.h>
#include <stdio.h>
#include <stddef.h>
long db_load(const char *path, unsigned char *out, size_t cap) {
    if (!path || !out || cap == 0) return -1;
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    unsigned char hdr[6];
    if (fread(hdr, 1, 6, f) != 6 || memcmp(hdr, "CJR1", 4) != 0) {
        fclose(f);
        return -1;
    }
    size_t claimed = hdr[4] | ((size_t)hdr[5] << 8);
    long loaded = 0;
    for (size_t i = 0; i < claimed && loaded < (long)cap; i++) {
        unsigned char rec[8];
        if (fread(rec, 1, 8, f) != 8) break;   /* truncated: stop cleanly */
        memcpy(out + (size_t)loaded * 8, rec, 8);
        loaded++;
    }
    fclose(f);
    return loaded;
}""",
    wrong=r"""
#include <string.h>
#include <stdio.h>
#include <stddef.h>
long db_load(const char *path, unsigned char *out, size_t cap) {
    if (!path || !out) return -1;              /* wrong: cap == 0 passes */
    FILE *f = fopen(path, "rb");
    if (!f) return -1;
    unsigned char hdr[6];
    fread(hdr, 1, 6, f);                       /* wrong: count unchecked —
                                                  a 3-byte file "reads" a header */
    if (memcmp(hdr, "CJR1", 4) != 0) {
        fclose(f);
        return -1;
    }
    size_t claimed = hdr[4] | ((size_t)hdr[5] << 8);
    if (claimed > cap) claimed = cap;          /* fine, but see below */
    for (size_t i = 0; i < claimed; i++) {
        unsigned char rec[8];
        fread(rec, 1, 8, f);                   /* wrong: short read ignored —
                                                  the tail of a truncated file
                                                  is filled with garbage and
                                                  reported as valid records */
        memcpy(out + i * 8, rec, 8);
    }
    fclose(f);
    return (long)claimed;
}""",
)

print("module 12 complete")
