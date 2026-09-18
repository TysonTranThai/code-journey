import type { HintLevel, MentorAdapter, MentorContext, MentorResponse } from "./types";

/**
 * NullMentor (AI-04): the no-key adapter. It still provides REAL value by
 * composing graduated hints from the challenge's own educational test hints
 * (content-as-data) — no fabricated API, no complete solutions, platform
 * fully functional.
 */
export const nullMentor: MentorAdapter = {
  async hint(context: MentorContext, level: HintLevel): Promise<MentorResponse> {
    const isVi = context.locale === "vi";
    const hints = context.testHints.filter((hint) => hint.length > 0);
    const first =
      hints[0] ??
      (isVi
        ? "Hãy đọc lại các yêu cầu của thử thách từng dòng một."
        : "Re-read the challenge requirements one line at a time.");

    if (isVi) {
      if (level === 1) {
        return {
          text: `Hãy cùng suy nghĩ nhé. Thử thách "${context.challengeTitle}" yêu cầu bạn thay đổi mã để đáp ứng tất cả yêu cầu. Trước tiên hãy xác định phần tử mà yêu cầu đầu tiên đề cập đến, sau đó đối chiếu với mã nguồn hiện tại của bạn. (Gợi ý 2 sẽ chỉ rõ hơn.)`,
        };
      }
      if (level === 2) {
        return {
          text: `Hãy tập trung vào yêu cầu này: ${first} Hãy so sánh với phiên bản chính xác — thẻ hoặc thuộc tính nào cần điều chỉnh?`,
        };
      }
      return {
        text: `Bạn rất gần đích rồi. Yêu cầu cần đáp ứng: ${first} Chỉ viết đúng một thay đổi đó, chạy lại kiểm thử và xem còn yêu cầu nào chưa đạt.`,
      };
    }

    if (level === 1) {
      return {
        text: `Let's think it through. ${context.challengeTitle} asks you to change the markup so every requirement passes. Start by identifying which element the first requirement talks about, then check what your code currently outputs. (Hint 2 will point closer.)`,
      };
    }
    if (level === 2) {
      return {
        text: `Focus on this requirement: ${first} Compare it with what a correct version would look like — which tag or attribute is involved?`,
      };
    }
    return {
      text: `You're close. The requirement to satisfy: ${first} Write just that one change, run the tests again, and see which requirement (if any) still complains.`,
    };
  },

  async explainError(
    context: MentorContext,
    failedTestName: string,
    errorOutput: string,
  ): Promise<MentorResponse> {
    const isVi = context.locale === "vi";
    const relevant =
      context.testHints.find(
        (hint) => failedTestName && failedTestName.length > 0 && hint.length > 0,
      ) ??
      context.testHints[0] ??
      "";

    if (isVi) {
      return {
        text: [
          `Bài kiểm tra bị trượt "${failedTestName}" đang kiểm tra một yêu cầu cụ thể.`,
          errorOutput.trim().length > 0
            ? `Thông báo lỗi chính là gợi ý đắt giá nhất: "${errorOutput.trim().slice(0, 200)}". Thông báo lỗi cho biết điểm khác biệt giữa kết quả mong đợi và kết quả thực tế từ mã của bạn.`
            : "Hãy đối chiếu kết quả bài test mong đợi so với những gì mã của bạn tạo ra.",
          relevant ? `Ghi nhớ: ${relevant}` : "",
          "Hãy sửa đúng yêu cầu đó, chạy lại kiểm thử và đọc thông báo tiếp theo nếu còn bài kiểm tra chưa đạt.",
        ]
          .filter(Boolean)
          .join(" "),
      };
    }

    return {
      text: [
        `The failing test "${failedTestName}" checks one specific requirement.`,
        errorOutput.trim().length > 0
          ? `The error message is your best clue: "${errorOutput.trim().slice(0, 200)}". Errors tell you what the test expected versus what it found.`
          : "Compare what the test expected against what your code produces.",
        relevant ? `Remember: ${relevant}` : "",
        "Fix that one requirement, run again, and read the next message if another test complains.",
      ]
        .filter(Boolean)
        .join(" "),
    };
  },
};
