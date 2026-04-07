# Test Results

## Test 1 – Direct Answer (Không cần tool)

- User: "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."
- Kỳ vọng: Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.

```txt
Bạn: Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Chào bạn! Có rất nhiều điểm đến thú vị ở Việt Nam để bạn khám phá. Bạn thích biển, núi rừng hay các thành phố với văn hóa đặc sắc hơn? Hoặc bạn đang tìm kiếm một nơi nào đó để thư giãn, ăn uống hay khám phá thiên nhiên? Hãy cho mình biết sở thích của bạn nhé!
```

## Test 2 – Single Tool Call

- User: "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"
- Kỳ vọng: Gọi search_flights("Hà Nội", "Đà Nẵng"), liệt kê 4 chuyến bay.

```txt
Bạn: Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Trả lời trực tiếp

TravelBuddy: Dưới đây là các chuyến bay từ Hà Nội đến Đà Nẵng:

1. **Vietnam Airlines**: 06:00 - 07:20 | Giá: 1.450.000 VNĐ | Hạng phổ thông
2. **Vietnam Airlines**: 14:00 - 15:20 | Giá: 2.800.000 VNĐ | Hạng thương gia
3. **VietJet Air**: 08:30 - 09:50 | Giá: 890.000 VNĐ | Hạng phổ thông
4. **Bamboo Airways**: 11:00 - 12:20 | Giá: 1.200.000 VNĐ | Hạng phổ thông

Bạn muốn đặt chuyến bay nào không? Hay cần thêm thông tin gì khác?
```

## Test 3 – Multi-Step Tool Chaining

- User: "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"
- Kỳ vọng: Agent phải tự chuỗi nhiều bước:
    1. search_flights("Hà Nội", "Phú Quốc") $\rightarrow$ tìm vé rẻ nhất (1.100.000đ)
    2. Google Hotels("Phú Quốc", max_price phù hợp) $\rightarrow$ gợi ý trong tầm giá
    3. calculate_budget(5000000, "vé_bay:1100000, khách_sạn:...") $\rightarrow$ tính còn lại
- Kết quả: Tổng hợp thành gợi ý hoàn chỉnh với bảng chi phí.

```txt
Bạn: Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

TravelBuddy đang suy nghĩ...
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Gọi tool: search_hotels({'city': 'Phú Quốc'})
Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:1600000'})
Trả lời trực tiếp

TravelBuddy: Dưới đây là kế hoạch cho chuyến đi của bạn từ Hà Nội đến Phú Quốc:

**Chuyến bay:**
- **VietJet Air:** 16:00 - 18:15 | Giá: 1,100,000đ (economy)

**Khách sạn:**
- **Lahana Resort:** 3 sao | Giá: 800,000đ/đêm | Dương Đông | Rating: 4.0
- Tổng chi phí cho 2 đêm là: 1,600,000đ

**Tổng chi phí ước tính:**
- Vé máy bay: 1,100,000đ
- Khách sạn: 1,600,000đ
- **Tổng chi: 2,700,000đ**

Bạn vẫn còn lại: **2,300,000đ** trong ngân sách 5 triệu.

Gợi ý thêm: Với số tiền còn lại, bạn có thể tận hưởng thêm nhiều hoạt động trên đảo như tham gia tour khám phá, ăn seafood, hay thư giãn tại bãi biển. Nếu bạn cần thêm thông tin gì, cứ hỏi mình nhé!
```

## Test 4 – Missing Info / Clarification

- User: "Tôi muốn đặt khách sạn"
- Kỳ vọng: Agent hỏi lại: thành phố nào? bao nhiêu đêm? ngân sách bao nhiêu? Không gọi tool vội.

```txt
Bạn: Tôi muốn đặt khách sạn

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Bạn có thể cho mình biết thành phố mà bạn muốn đặt khách sạn không?
```

## Test 5 – Guardrail / Refusal

- User: "Giải giúp tôi bài tập lập trình Python về linked list"
- Kỳ vọng: Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

```txt
Bạn: Giải giúp tôi bài tập lập trình Python về linked list

TravelBuddy đang suy nghĩ...
Trả lời trực tiếp

TravelBuddy: Xin lỗi, nhưng mình không thể giúp bạn với bài tập lập trình hay những vấn đề liên quan đến kỹ thuật khác. Tuy nhiên, nếu bạn có kế hoạch đi du lịch hoặc cần hỗ trợ về đặt vé máy bay, khách sạn, mình rất vui được giúp đỡ! Bạn có điểm đến nào không?
```
