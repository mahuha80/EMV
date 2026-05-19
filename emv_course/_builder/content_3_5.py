"""Content for Lessons 3-5"""

# ============================================================
# LESSON 3: Transaction Flow
# ============================================================
LESSON_03 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Hiểu 8 bước của một giao dịch EMV theo EMV Book 3.</li>
        <li>Phân biệt được hai nhánh: online authorization vs offline approval.</li>
        <li>Hiểu vai trò của các cryptogram TC, ARQC, AAC.</li>
        <li>Đọc được TVR, TSI, CVM Results để debug giao dịch.</li>
    </ul>
</div>

<div class="section">
    <h2>📊 Tổng quan — 8 bước theo EMV Book 3</h2>
    <p>EMV Book 3 (“Application Specification”) định nghĩa thứ tự xử lý một giao dịch contact. Contactless rút gọn flow này (kernel-specific) nhưng tinh thần không đổi:</p>

    <div class="flow-step"><div class="step-number">1</div>
        <div class="step-content"><h4>Application Selection</h4>
        <p>Terminal chọn application: SELECT PPSE/PSE → SELECT AID. Kết quả: terminal biết AID, có FCI và PDOL.</p></div>
    </div>
    <div class="flow-step"><div class="step-number">2</div>
        <div class="step-content"><h4>Initiate Application Processing</h4>
        <p>Terminal gửi GET PROCESSING OPTIONS (GPO) với dữ liệu PDOL. Card trả về AIP + AFL.</p></div>
    </div>
    <div class="flow-step"><div class="step-number">3</div>
        <div class="step-content"><h4>Read Application Data</h4>
        <p>Terminal đọc các record theo AFL bằng READ RECORD. Kết quả: PAN, expiry, CVM list, certificate, public key…</p></div>
    </div>
    <div class="flow-step"><div class="step-number">4</div>
        <div class="step-content"><h4>Offline Data Authentication (ODA)</h4>
        <p>SDA, DDA hoặc CDA — terminal verify chữ ký RSA để chắc rằng thẻ thật. Bài 7 đi sâu phần này.</p></div>
    </div>
    <div class="flow-step"><div class="step-number">5</div>
        <div class="step-content"><h4>Processing Restrictions</h4>
        <p>Check version, usage control, country code, expiry date. Nếu fail thì set bit tương ứng trong TVR.</p></div>
    </div>
    <div class="flow-step"><div class="step-number">6</div>
        <div class="step-content"><h4>Cardholder Verification (CVM)</h4>
        <p>Verify chủ thẻ theo CVM List của thẻ: Offline PIN, Online PIN, Signature, CDCVM, hoặc No CVM.</p></div>
    </div>
    <div class="flow-step"><div class="step-number">7</div>
        <div class="step-content"><h4>Terminal Risk Management + Terminal Action Analysis</h4>
        <p>Terminal kiểm tra floor limit, velocity, random selection, log. Sau đó quyết định: chấp nhận offline (TC), gửi online (ARQC), hay từ chối (AAC).</p></div>
    </div>
    <div class="flow-step"><div class="step-number">8</div>
        <div class="step-content"><h4>Card Action Analysis + Online + Completion</h4>
        <p>Terminal gọi GENERATE AC. Card phản hồi cryptogram. Nếu ARQC → online authorization với issuer, sau đó terminal gọi GENERATE AC lần 2 để completion.</p></div>
    </div>
</div>

<div class="section">
    <h2>🔍 Bước 1 — Application Selection</h2>
    <p>Bài 2 đã giới thiệu PPSE. Ở đây ta xem dữ liệu thật:</p>

    <div class="code-block"><span class="comment">// 1. SELECT PPSE (contactless entry point)</span>
&gt;&gt; <span class="hex">00 A4 04 00 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31 00</span>

<span class="comment">// Card response — FCI Template</span>
&lt;&lt; <span class="hex">6F 23
      84 0E 32 50 41 59 2E 53 59 53 2E 44 44 46 30 31
      A5 11
         BF 0C 0E
            61 0C
               4F 07 A0 00 00 00 03 10 10
               87 01 01
   90 00</span>

<span class="comment">// Phân rã:</span>
<span class="hex">6F</span>  FCI Template
  <span class="hex">84</span>  DF Name = "2PAY.SYS.DDF01"
  <span class="hex">A5</span>  FCI Proprietary Template
    <span class="hex">BF 0C</span>  FCI Issuer Discretionary Data
      <span class="hex">61</span>  Application Template (lặp lại theo số AID)
        <span class="hex">4F</span>  AID = A0000000031010 (Visa)
        <span class="hex">87</span>  Priority = 01</div>

    <p>Nếu thẻ trả về nhiều <code>61</code>, terminal chọn AID có priority thấp nhất (1 là ưu tiên cao nhất). Sau đó SELECT trực tiếp AID đó:</p>

    <div class="code-block"><span class="comment">// 2. SELECT AID</span>
&gt;&gt; <span class="hex">00 A4 04 00 07 A0 00 00 00 03 10 10 00</span>

&lt;&lt; <span class="hex">6F 35
      84 07 A0 00 00 00 03 10 10
      A5 2A
         50 0B 56 49 53 41 20 43 52 45 44 49 54   <span class="comment">// "VISA CREDIT"</span>
         87 01 01
         5F 2D 02 65 6E                            <span class="comment">// Language "en"</span>
         9F 38 0F 9F 66 04 9F 02 06 9F 03 06 9F 1A 02 95 05 5F 2A 02 9A 03 9C 01 9F 37 04
   90 00</span>

<span class="hex">9F 38</span> là <strong>PDOL</strong> — danh sách tag mà terminal phải nhồi dữ liệu để gửi vào lệnh GPO ở bước sau.</div>
</div>

<div class="section">
    <h2>🔍 Bước 2 — GET PROCESSING OPTIONS (GPO)</h2>
    <p>Terminal build PDOL data theo đúng thứ tự tag-length trong <code>9F38</code>, đóng gói trong template <code>83</code>:</p>

    <div class="code-block"><span class="comment">// PDOL yêu cầu các tag (đã trả về ở bước SELECT AID):</span>
<span class="comment">// 9F66 (4)   - TTQ (Terminal Transaction Qualifiers)</span>
<span class="comment">// 9F02 (6)   - Amount Authorized</span>
<span class="comment">// 9F03 (6)   - Amount Other</span>
<span class="comment">// 9F1A (2)   - Terminal Country Code</span>
<span class="comment">// 95   (5)   - TVR</span>
<span class="comment">// 5F2A (2)   - Transaction Currency Code</span>
<span class="comment">// 9A   (3)   - Transaction Date</span>
<span class="comment">// 9C   (1)   - Transaction Type</span>
<span class="comment">// 9F37 (4)   - Unpredictable Number</span>

<span class="comment">// Tổng độ dài data = 4+6+6+2+5+2+3+1+4 = 33 byte</span>

&gt;&gt; <span class="hex">80 A8 00 00 23 83 21
      36 00 40 80                  <span class="comment">// TTQ - supports VSDC, online PIN</span>
      00 00 00 10 00 00            <span class="comment">// 100,000 đồng = 100000 minor units</span>
      00 00 00 00 00 00            <span class="comment">// No "amount other"</span>
      07 04                         <span class="comment">// 0704 = Vietnam (ISO 3166-1 numeric)</span>
      00 00 00 00 00               <span class="comment">// TVR all zero (chưa check gì)</span>
      07 04                         <span class="comment">// Currency VND (ISO 4217 numeric)</span>
      26 05 19                      <span class="comment">// Date YYMMDD = 2026-05-19</span>
      00                            <span class="comment">// 00 = Purchase</span>
      11 22 33 44                   <span class="comment">// Random UN</span>
      00</span>

<span class="comment">// Card response (định dạng 2 - template 77)</span>
&lt;&lt; <span class="hex">77 16
      82 02 1980                   <span class="comment">// AIP</span>
      94 10 08 01 01 00  10 01 04 01  18 01 01 00  20 01 02 00
   90 00</span></div>

    <h3>AIP — Application Interchange Profile (tag <code>82</code>)</h3>
    <p>2 byte bitmap, mô tả khả năng của application:</p>
    <table>
        <tr><th>Byte 1 bit</th><th>Ý nghĩa</th></tr>
        <tr><td>b7</td><td>SDA supported</td></tr>
        <tr><td>b6</td><td>DDA supported</td></tr>
        <tr><td>b5</td><td>Cardholder verification supported</td></tr>
        <tr><td>b4</td><td>Terminal risk management to be performed</td></tr>
        <tr><td>b3</td><td>Issuer authentication supported</td></tr>
        <tr><td>b1</td><td>CDA supported</td></tr>
    </table>
    <p>Ví dụ AIP = <code>19 80</code> = <code>0001 1001 1000 0000</code>: DDA + CVM + Issuer Auth + CDA.</p>

    <h3>AFL — Application File Locator (tag <code>94</code>)</h3>
    <p>Danh sách record cần đọc. Mỗi mục 4 byte:</p>
    <div class="code-block"><span class="hex">08 01 01 00</span>  →  SFI=1, record 1 đến 1, 0 record nằm trong phạm vi offline data auth
<span class="hex">10 01 04 01</span>  →  SFI=2, record 1 đến 4, record đầu nằm trong ODA
<span class="hex">18 01 01 00</span>  →  SFI=3, record 1 đến 1, 0 trong ODA
<span class="hex">20 01 02 00</span>  →  SFI=4, record 1 đến 2, 0 trong ODA

<span class="comment">// Byte 1: SFI dịch trái 3 bit (vì SFI nằm ở 5 bit cao)
// Byte 2: first record
// Byte 3: last record
// Byte 4: số record đầu tiên thuộc Offline Data Authentication</span></div>
</div>

<div class="section">
    <h2>🔍 Bước 3 — READ RECORD</h2>
    <p>Terminal duyệt từng mục AFL, gọi READ RECORD:</p>

    <div class="code-block"><span class="comment">// P2 = (SFI << 3) | 0x04  → cho biết "đọc bằng SFI"</span>
<span class="comment">// SFI=1 → P2 = 0x0C; SFI=2 → P2=0x14; SFI=3 → P2=0x1C; SFI=4 → P2=0x24</span>

&gt;&gt; <span class="hex">00 B2 01 0C 00</span>     <span class="comment">// READ RECORD 1 của SFI 1</span>

&lt;&lt; <span class="hex">70 5C
      5A 08 45 32 12 34 56 78 90 10
      5F 24 03 27 12 31                                  <span class="comment">// Expiry 2027-12-31</span>
      5F 25 03 22 01 01                                  <span class="comment">// Effective 2022-01-01</span>
      5F 28 02 07 04                                     <span class="comment">// Issuer country = VN</span>
      5F 34 01 01                                        <span class="comment">// PAN Sequence Number</span>
      5F 20 14 4E 47 55 59 45 4E 2F 56 41 4E 20 41 20 20 20 20 20 20 20 20  <span class="comment">// "NGUYEN/VAN A"</span>
      8C 1B ... (CDOL1) ...
      8D 0C ... (CDOL2) ...
      8E 0E 00 00 00 00 00 00 00 00 42 03 1E 03 1F 00     <span class="comment">// CVM List</span>
   90 00</span></div>

    <p><strong>Template <code>70</code></strong> là "Record Template" — luôn bọc dữ liệu của một record.</p>
</div>

<div class="section">
    <h2>🔍 Bước 6 — Cardholder Verification (CVM)</h2>
    <p>Tag <code>8E</code> là <strong>CVM List</strong>: 8 byte header (Amount X, Amount Y) + danh sách CV Rules, mỗi rule 2 byte.</p>

    <table>
        <tr><th>CVM Code (byte 1, lower 6 bits)</th><th>Method</th></tr>
        <tr><td><code>00</code></td><td>Fail CVM processing</td></tr>
        <tr><td><code>01</code></td><td>Plaintext PIN verification — offline</td></tr>
        <tr><td><code>02</code></td><td>Enciphered PIN — online</td></tr>
        <tr><td><code>03</code></td><td>Plaintext PIN + signature — offline</td></tr>
        <tr><td><code>04</code></td><td>Enciphered PIN — offline</td></tr>
        <tr><td><code>05</code></td><td>Enciphered PIN + signature — offline</td></tr>
        <tr><td><code>1E</code></td><td>Signature (paper)</td></tr>
        <tr><td><code>1F</code></td><td>No CVM required</td></tr>
    </table>

    <div class="info-box">
        <h3>📱 CDCVM là gì?</h3>
        <p><strong>CDCVM</strong> = Consumer Device CVM. Khi bạn unlock điện thoại bằng FaceID/vân tay để tap Apple Pay/Google Pay, kernel hiểu rằng cardholder đã được verify <em>trên thiết bị</em>, không cần PIN trên POS. Được biểu thị qua bit trong TTQ và Card Transaction Qualifiers (CTQ).</p>
    </div>

    <h3>Offline PIN verification</h3>
    <div class="code-block"><span class="comment">// VERIFY APDU — gửi PIN trực tiếp cho chip để check offline</span>
&gt;&gt; <span class="hex">00 20 00 80 08 24 12 34 FF FF FF FF FF</span>
                    └─ PIN block format 2 (ISO 9564-1):
                       2 = format, 4 = length, 1234 = digits, padding 'F'

&lt;&lt; <span class="hex">90 00</span>   <span class="comment">// PIN đúng</span>
&lt;&lt; <span class="hex">63 C2</span>   <span class="comment">// Sai — còn 2 lần thử (C = counter prefix)</span>
&lt;&lt; <span class="hex">69 83</span>   <span class="comment">// PIN bị khóa</span></div>
</div>

<div class="section">
    <h2>🔍 Bước 7-8 — Cryptogram (GENERATE AC)</h2>
    <p>Đây là trái tim bảo mật của EMV. Terminal gọi <strong>GENERATE AC</strong> với CDOL1 data, yêu cầu một trong ba loại cryptogram:</p>

    <table>
        <tr><th>Cryptogram</th><th>CID byte</th><th>Ý nghĩa</th></tr>
        <tr><td><strong>AAC</strong></td><td>00xx xxxx</td><td>Application Authentication Cryptogram — Decline</td></tr>
        <tr><td><strong>TC</strong></td><td>01xx xxxx</td><td>Transaction Certificate — Approve offline</td></tr>
        <tr><td><strong>ARQC</strong></td><td>10xx xxxx</td><td>Authorization Request Cryptogram — Go online</td></tr>
    </table>

    <h3>Reference Control Parameter (P1 của GENERATE AC)</h3>
    <table>
        <tr><th>P1</th><th>Terminal yêu cầu</th></tr>
        <tr><td><code>00</code></td><td>AAC</td></tr>
        <tr><td><code>40</code></td><td>TC</td></tr>
        <tr><td><code>80</code></td><td>ARQC</td></tr>
        <tr><td><code>50</code></td><td>TC + request CDA signature</td></tr>
        <tr><td><code>90</code></td><td>ARQC + CDA</td></tr>
    </table>

    <div class="warning-box">
        <h3>⚠️ Card có quyền “down-grade”</h3>
        <p>Terminal yêu cầu TC, nhưng nếu card áp dụng risk management thấy bất thường (offline counter quá cao chẳng hạn), card có thể trả về ARQC ép online — hoặc AAC để decline. Terminal <strong>không có quyền</strong> override.</p>
    </div>

    <h3>Cách cryptogram được tạo</h3>
    <div class="code-block"><span class="comment">// 1. Derive một Application Cryptogram Key (AC Key) duy nhất cho card</span>
<span class="comment">//    từ Issuer Master Key (IMK) và PAN + PAN Sequence Number</span>
UDK = 3DES_Encrypt(IMK, PAN || PSN)

<span class="comment">// 2. Derive Session Key từ UDK và ATC (Application Transaction Counter)</span>
SK_AC = SessionKeyDerive(UDK, ATC)   <span class="comment">// EMV Common Session Key Derivation</span>

<span class="comment">// 3. Build input data từ CDOL1 (amount, country, TVR, currency, date,
//    type, UN, AIP, ATC, CVR, ...)</span>
data = CDOL1_data || AIP || ATC || IAD_internal

<span class="comment">// 4. Tính cryptogram (MAC theo ISO/IEC 9797-1 Algorithm 3)</span>
cryptogram = MAC(SK_AC, data)[0..8]   <span class="comment">// 8 byte đầu</span></div>

    <p>Cryptogram được trả về tag <code>9F26</code>, CID ở <code>9F27</code>, ATC ở <code>9F36</code>:</p>

    <div class="code-block">&lt;&lt; <span class="hex">77 47
      9F 27 01 80                                     <span class="comment">// CID = 80 → ARQC</span>
      9F 36 02 00 1A                                  <span class="comment">// ATC = 26</span>
      9F 26 08 A1 B2 C3 D4 E5 F6 07 18                <span class="comment">// Cryptogram</span>
      9F 10 12 06 01 0A 03 A4 00 00 00 00 00 00 00 00 00 FF
   90 00</span></div>

    <h3>Online authorization</h3>
    <p>Khi nhận ARQC, terminal gửi message ISO 8583 (DE 55 chứa ARQC + các tag liên quan) qua acquirer → network → issuer. Issuer dùng IMK + ATC + PAN để tái tạo SK_AC, verify cryptogram, sau đó trả về:</p>
    <ul>
        <li><strong>Authorization Response Code (ARC)</strong> — 2 byte ASCII: "00" = approved, "05" = declined…</li>
        <li><strong>ARPC</strong> — Authorization Response Cryptogram, do issuer ký, để chứng minh response thật sự từ issuer.</li>
        <li>Optional: <strong>Issuer Scripts</strong> để update card từ xa (đổi key, unlock PIN…).</li>
    </ul>
    <p>Terminal gọi GENERATE AC lần 2 với ARPC để card verify và return TC nếu OK.</p>
</div>

<div class="section">
    <h2>📊 TVR & TSI — Hai bitmap bạn sẽ gặp hằng ngày</h2>
    <p><strong>TVR</strong> (Terminal Verification Results, tag <code>95</code>, 5 byte) — Terminal đánh bit lên TVR khi có vấn đề: offline auth fail, expired card, exceeds floor limit, PIN try limit exceeded… 5 byte tổng cộng 40 bit.</p>
    <p><strong>TSI</strong> (Transaction Status Information, tag <code>9B</code>, 2 byte) — đánh dấu các bước nào <em>đã được thực hiện</em>: ODA performed, CVM performed, Risk Management performed…</p>

    <div class="info-box">
        <h3>🔧 Debug bằng TVR</h3>
        <p>Khi giao dịch bị decline mà không rõ lý do, dán TVR vào một tool decode (như emvlab.org/tlvutils) sẽ thấy ngay bit nào được set, ví dụ <code>95 = 00 00 00 80 00</code> → bit "Exceeds floor limit".</p>
    </div>
</div>

<div class="term-box">
    <h3>📘 Thuật ngữ bài này</h3>
    <dl>
        <dt>GPO</dt>
        <dd>GET PROCESSING OPTIONS (INS = A8) — lệnh khởi động application processing.</dd>

        <dt>AIP</dt>
        <dd>Application Interchange Profile, tag <code>82</code>, 2 byte. Mô tả khả năng app (SDA/DDA/CDA, CVM, issuer auth).</dd>

        <dt>AFL</dt>
        <dd>Application File Locator, tag <code>94</code>. Danh sách record cần đọc.</dd>

        <dt>CDOL1 / CDOL2</dt>
        <dd>Card Risk Management Data Object List 1 và 2 — danh sách tag mà terminal phải gửi trong GENERATE AC lần 1 và lần 2.</dd>

        <dt>TC / ARQC / AAC</dt>
        <dd>Transaction Certificate / Authorization Request Cryptogram / Application Authentication Cryptogram — 3 loại cryptogram do card sinh, phân biệt qua CID (tag <code>9F27</code>).</dd>

        <dt>ATC</dt>
        <dd>Application Transaction Counter, tag <code>9F36</code> — biến đếm 2 byte, mỗi giao dịch tăng 1. Đảm bảo session key luôn khác nhau.</dd>

        <dt>UN</dt>
        <dd>Unpredictable Number, tag <code>9F37</code>, 4 byte. Terminal random mỗi giao dịch, đảm bảo cryptogram khác nhau cả khi cùng amount.</dd>

        <dt>TVR</dt>
        <dd>Terminal Verification Results, tag <code>95</code>, 5 byte bitmap — terminal đánh dấu các bất thường.</dd>

        <dt>TSI</dt>
        <dd>Transaction Status Information, tag <code>9B</code>, 2 byte — đánh dấu các bước nào đã thực hiện.</dd>

        <dt>ARC</dt>
        <dd>Authorization Response Code — 2 ký tự ASCII trả về từ issuer.</dd>

        <dt>ARPC</dt>
        <dd>Authorization Response Cryptogram — chữ ký của issuer trên ARQC + ARC, để card verify.</dd>

        <dt>Issuer Script</dt>
        <dd>Lệnh đặc biệt do issuer gửi xuống thẻ qua kênh online (tag <code>71</code> = pre-GAC, <code>72</code> = post-GAC). Dùng để update key, reset PIN counter, block app.</dd>
    </dl>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>AIP = <code>5C 00</code> — app này hỗ trợ SDA/DDA/CDA gì?</li>
        <li>AFL = <code>10 01 03 01 18 01 01 00</code> — terminal phải gửi mấy lệnh READ RECORD?</li>
        <li>CID = <code>40</code> — card trả lời gì?</li>
        <li>Tìm hiểu sự khác nhau giữa response format 1 (template <code>80</code>) và format 2 (template <code>77</code>) của GPO.</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>EMV Book 3 chuẩn hóa 8 bước: SELECT → GPO → READ RECORD → ODA → restrictions → CVM → risk → GENERATE AC.</li>
        <li>3 loại cryptogram: TC (approve offline), ARQC (go online), AAC (decline). Phân biệt qua CID.</li>
        <li>ARQC được issuer verify; issuer trả ARC + ARPC; terminal gọi GENERATE AC lần 2 để completion.</li>
        <li>TVR và TSI là 2 bitmap không thể thiếu khi debug giao dịch.</li>
    </ul>
</div>
'''


# ============================================================
# LESSON 4: APDU Commands
# ============================================================
LESSON_04 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Hiểu cấu trúc Command APDU và Response APDU theo ISO/IEC 7816-4.</li>
        <li>Phân biệt 4 dạng C-APDU (Case 1–4) và short vs extended length.</li>
        <li>Học chi tiết các APDU dùng trong EMV: SELECT, GPO, READ RECORD, GENERATE AC, INTERNAL AUTHENTICATE, VERIFY, GET DATA.</li>
        <li>Đọc và hiểu status word SW1-SW2.</li>
    </ul>
</div>

<div class="section">
    <h2>📦 Cấu trúc APDU (ISO/IEC 7816-4)</h2>

    <h3>Command APDU (C-APDU)</h3>
    <div class="diagram"><pre>
┌──── Header (4 byte bắt buộc) ────┐  ┌────── Body (tùy chọn) ──────┐
│  CLA  │  INS  │  P1   │  P2     │  │  [Lc]   [Data]   [Le]       │
└───────┴───────┴───────┴─────────┘  └─────────────────────────────┘
   1B      1B      1B      1B           1-3B    0-65535B    1-3B
    </pre></div>

    <table>
        <tr><th>Trường</th><th>Ý nghĩa</th></tr>
        <tr><td><strong>CLA</strong></td><td>Class byte — quy định bộ lệnh và secure messaging</td></tr>
        <tr><td><strong>INS</strong></td><td>Instruction byte — mã lệnh</td></tr>
        <tr><td><strong>P1, P2</strong></td><td>Parameter 1, 2 — tham số tùy theo INS</td></tr>
        <tr><td><strong>Lc</strong></td><td>Length of Command data — chỉ có nếu có Data</td></tr>
        <tr><td><strong>Data</strong></td><td>Data field</td></tr>
        <tr><td><strong>Le</strong></td><td>Expected length of response — <code>00</code> = "tối đa" (256 byte với short, 65536 với extended)</td></tr>
    </table>

    <h3>4 Cases (ISO 7816-4 §5.1)</h3>
    <table>
        <tr><th>Case</th><th>Data từ terminal</th><th>Data từ card</th><th>Layout</th></tr>
        <tr><td>1</td><td>Không</td><td>Không</td><td>CLA INS P1 P2</td></tr>
        <tr><td>2</td><td>Không</td><td>Có</td><td>CLA INS P1 P2 Le</td></tr>
        <tr><td>3</td><td>Có</td><td>Không</td><td>CLA INS P1 P2 Lc Data</td></tr>
        <tr><td>4</td><td>Có</td><td>Có</td><td>CLA INS P1 P2 Lc Data Le</td></tr>
    </table>

    <h3>Response APDU (R-APDU)</h3>
    <div class="diagram"><pre>
┌────────── Data ──────────┐ ┌── SW1 ──┐ ┌── SW2 ──┐
│   0 hoặc nhiều byte      │ │   1B    │ │   1B    │
└──────────────────────────┘ └─────────┘ └─────────┘
    </pre></div>

    <p>SW1-SW2 luôn có. Data có thể rỗng (nhiều lệnh chỉ trả status).</p>

    <h3>Status Words quan trọng (ISO 7816-4 §5.1.3 + EMV Book 1)</h3>
    <table>
        <tr><th>SW1 SW2</th><th>Ý nghĩa</th></tr>
        <tr><td><code>90 00</code></td><td>Success — không thêm thông tin</td></tr>
        <tr><td><code>61 XX</code></td><td>Process completed normally, còn XX byte sẵn sàng — gọi GET RESPONSE</td></tr>
        <tr><td><code>62 83</code></td><td>State of non-volatile memory unchanged; selected file deactivated</td></tr>
        <tr><td><code>63 CX</code></td><td>Verification failed, còn X lần thử (X = 0 → blocked)</td></tr>
        <tr><td><code>67 00</code></td><td>Wrong length (Lc hoặc Le sai)</td></tr>
        <tr><td><code>69 81</code></td><td>Command incompatible with file structure</td></tr>
        <tr><td><code>69 82</code></td><td>Security status not satisfied</td></tr>
        <tr><td><code>69 83</code></td><td>Authentication method blocked</td></tr>
        <tr><td><code>69 84</code></td><td>Reference data invalidated</td></tr>
        <tr><td><code>69 85</code></td><td>Conditions of use not satisfied</td></tr>
        <tr><td><code>69 86</code></td><td>Command not allowed (no current EF)</td></tr>
        <tr><td><code>6A 80</code></td><td>Incorrect parameters in data field</td></tr>
        <tr><td><code>6A 81</code></td><td>Function not supported</td></tr>
        <tr><td><code>6A 82</code></td><td>File or application not found</td></tr>
        <tr><td><code>6A 83</code></td><td>Record not found</td></tr>
        <tr><td><code>6A 86</code></td><td>Incorrect P1-P2</td></tr>
        <tr><td><code>6A 88</code></td><td>Referenced data not found</td></tr>
        <tr><td><code>6C XX</code></td><td>Wrong Le, the right length is XX — gửi lại với Le = XX</td></tr>
        <tr><td><code>6D 00</code></td><td>Instruction code not supported or invalid</td></tr>
        <tr><td><code>6E 00</code></td><td>Class not supported</td></tr>
        <tr><td><code>6F 00</code></td><td>No precise diagnosis</td></tr>
    </table>
</div>

<div class="section">
    <h2>🎯 SELECT (INS = <code>A4</code>) — chọn ứng dụng/file</h2>

    <h3>P1 — selection mode</h3>
    <table>
        <tr><th>P1</th><th>Ý nghĩa</th></tr>
        <tr><td><code>00</code></td><td>Select MF, DF, EF bằng file identifier (2 byte)</td></tr>
        <tr><td><code>01</code></td><td>Select child DF</td></tr>
        <tr><td><code>02</code></td><td>Select EF dưới DF hiện hành</td></tr>
        <tr><td><code>03</code></td><td>Select parent DF</td></tr>
        <tr><td><code>04</code></td><td><strong>Select by DF Name / AID</strong> (dùng nhiều nhất trong EMV)</td></tr>
    </table>

    <h3>P2 — selection options</h3>
    <p>EMV mặc định <code>P2 = 00</code> = "return FCI template, first or only occurrence".</p>

    <div class="code-block"><span class="comment">// Ví dụ: SELECT Visa Credit AID</span>
&gt;&gt; <span class="hex">00 A4 04 00 07 A0 00 00 00 03 10 10 00</span>
   │  │  │  │  │  └────────────┬───────┘  │
   │  │  │  │  │               │          └─ Le = 00 (xin tối đa 256 byte)
   │  │  │  │  │               └─ Data = AID
   │  │  │  │  └─ Lc = 7 byte
   │  │  │  └─ P2 = 00 (FCI, first)
   │  │  └─ P1 = 04 (select by name)
   │  └─ INS = A4
   └─ CLA = 00 (ISO standard)</div>
</div>

<div class="section">
    <h2>🎯 GET PROCESSING OPTIONS (CLA=<code>80</code>, INS=<code>A8</code>)</h2>
    <p>Lệnh "proprietary" của EMV (vì CLA = 80, không phải ISO standard 00). P1=P2=00.</p>

    <div class="code-block"><span class="comment">// Data luôn nằm trong template 83 (PDOL Related Data)</span>
&gt;&gt; <span class="hex">80 A8 00 00 Lc 83 (Lc-2) [PDOL_data] 00</span>

<span class="comment">// Nếu PDOL rỗng (thẻ không yêu cầu data):</span>
&gt;&gt; <span class="hex">80 A8 00 00 02 83 00 00</span></div>

    <h3>Response — 2 định dạng</h3>
    <table>
        <tr><th>Format</th><th>Template</th><th>Cấu trúc</th></tr>
        <tr><td>1</td><td><code>80</code></td><td>AIP (2 byte) || AFL (var) — không TLV, dữ liệu liền mạch</td></tr>
        <tr><td>2</td><td><code>77</code></td><td>TLV — có tag <code>82</code> (AIP), <code>94</code> (AFL) và có thể thêm tag khác</td></tr>
    </table>
</div>

<div class="section">
    <h2>🎯 READ RECORD (CLA=<code>00</code>, INS=<code>B2</code>)</h2>
    <p><strong>P1</strong> = record number. <strong>P2</strong> = <code>(SFI &lt;&lt; 3) | 0x04</code>.</p>

    <div class="code-block"><span class="comment">// Đọc record 2 của EF có SFI = 3</span>
P2 = (3 &lt;&lt; 3) | 0x04 = 0x1C
&gt;&gt; <span class="hex">00 B2 02 1C 00</span></div>

    <p>Nếu trả về <code>6C XX</code>, terminal gửi lại với Le = XX:</p>
    <div class="code-block">&lt;&lt; <span class="hex">6C 5A</span>                  <span class="comment">// "đúng length là 5A = 90 byte"</span>
&gt;&gt; <span class="hex">00 B2 02 1C 5A</span>        <span class="comment">// gửi lại với Le = 5A</span>
&lt;&lt; <span class="hex">70 ... 90 00</span></div>
</div>

<div class="section">
    <h2>🎯 GENERATE AC (CLA=<code>80</code>, INS=<code>AE</code>)</h2>
    <p>Đã giới thiệu ở bài 3. P1 quyết định loại cryptogram terminal yêu cầu.</p>

    <div class="code-block">&gt;&gt; <span class="hex">80 AE 80 00 Lc [CDOL1_data] 00</span>      <span class="comment">// P1=80 → request ARQC</span>
&gt;&gt; <span class="hex">80 AE 40 00 Lc [CDOL1_data] 00</span>      <span class="comment">// P1=40 → request TC (offline approve)</span>
&gt;&gt; <span class="hex">80 AE 00 00 Lc [CDOL1_data] 00</span>      <span class="comment">// P1=00 → request AAC (decline)</span>

<span class="comment">// Bit b6 của P1 = CDA Signature Requested
// → 50 = TC + CDA, 90 = ARQC + CDA</span></div>
</div>

<div class="section">
    <h2>🎯 INTERNAL AUTHENTICATE (CLA=<code>00</code>, INS=<code>88</code>)</h2>
    <p>Dùng cho DDA — terminal gửi data (DDOL data) cho card ký bằng ICC Private Key.</p>

    <div class="code-block">&gt;&gt; <span class="hex">00 88 00 00 Lc [DDOL_data] 00</span>

&lt;&lt; <span class="hex">80 81 80 [128 byte RSA-signed data] 90 00</span>
   <span class="comment">// Hoặc dạng TLV: 77 81 83 9F 4B 81 80 [...] 90 00
   // 9F4B = Signed Dynamic Application Data</span></div>
</div>

<div class="section">
    <h2>🎯 VERIFY (CLA=<code>00</code>, INS=<code>20</code>) — kiểm tra PIN</h2>
    <p>P2 quy định reference data (<code>80</code> = transaction PIN).</p>

    <div class="code-block">&gt;&gt; <span class="hex">00 20 00 80 08 [8 byte PIN block]</span>

<span class="comment">// PIN Block format 2 (ISO 9564-1):</span>
<span class="comment">// nibble[0]   = 2  (format code)
// nibble[1]   = N  (PIN length, ví dụ 4)
// nibble[2..N+1] = PIN digits
// nibble còn lại = F (pad)</span>

<span class="comment">// PIN "1234" → 24 12 34 FF FF FF FF FF</span></div>

    <p>Nếu dùng <strong>enciphered offline PIN</strong>, terminal phải encrypt PIN block bằng <strong>ICC PIN Encipherment Public Key</strong> (RSA) đọc từ card trước.</p>
</div>

<div class="section">
    <h2>🎯 GET DATA (CLA=<code>80</code>, INS=<code>CA</code>)</h2>
    <p>Đọc một data object cụ thể không nằm trong record. EMV chuẩn hóa 4 tag có thể đọc bằng GET DATA:</p>
    <table>
        <tr><th>Tag</th><th>Data</th></tr>
        <tr><td><code>9F36</code></td><td>ATC (Application Transaction Counter)</td></tr>
        <tr><td><code>9F13</code></td><td>Last Online ATC</td></tr>
        <tr><td><code>9F17</code></td><td>PIN Try Counter</td></tr>
        <tr><td><code>9F4F</code></td><td>Log Format</td></tr>
    </table>
    <div class="code-block"><span class="comment">// Đọc PIN Try Counter</span>
&gt;&gt; <span class="hex">80 CA 9F 17 00</span>
&lt;&lt; <span class="hex">9F 17 01 03 90 00</span>     <span class="comment">// còn 3 lần thử PIN</span></div>
</div>

<div class="section">
    <h2>🎯 GET RESPONSE (CLA=<code>00</code>, INS=<code>C0</code>)</h2>
    <p>Dùng với protocol T=0 sau khi nhận <code>61 XX</code>:</p>
    <div class="code-block">&lt;&lt; <span class="hex">61 1A</span>                    <span class="comment">// "Có 0x1A byte chờ"</span>
&gt;&gt; <span class="hex">00 C0 00 00 1A</span>
&lt;&lt; <span class="hex">[26 byte data] 90 00</span></div>
</div>

<div class="section">
    <h2>📱 Kotlin helper — APDU</h2>
    <div class="code-block">data class CommandApdu(
    val cla: Byte, val ins: Byte, val p1: Byte, val p2: Byte,
    val data: ByteArray? = null, val le: Int = -1
) {
    fun toBytes(): ByteArray {
        val out = mutableListOf&lt;Byte&gt;()
        out += cla; out += ins; out += p1; out += p2
        if (data != null) {
            out += data.size.toByte()
            out += data.toList()
        }
        if (le &gt;= 0) out += le.toByte()
        return out.toByteArray()
    }
}

data class ResponseApdu(val data: ByteArray, val sw1: Int, val sw2: Int) {
    val sw: Int get() = (sw1 shl 8) or sw2
    val isSuccess: Boolean get() = sw == 0x9000

    companion object {
        fun parse(bytes: ByteArray): ResponseApdu {
            require(bytes.size &gt;= 2)
            val sw1 = bytes[bytes.size - 2].toInt() and 0xFF
            val sw2 = bytes[bytes.size - 1].toInt() and 0xFF
            val data = bytes.copyOfRange(0, bytes.size - 2)
            return ResponseApdu(data, sw1, sw2)
        }
    }
}

<span class="comment">// Helper</span>
fun selectByAid(aid: ByteArray) =
    CommandApdu(0x00, 0xA4.toByte(), 0x04, 0x00, aid, 0x00).toBytes()

fun readRecord(sfi: Int, record: Int) =
    CommandApdu(0x00, 0xB2, record.toByte(), ((sfi shl 3) or 0x04).toByte(), null, 0x00).toBytes()</div>
</div>

<div class="term-box">
    <h3>📘 Thuật ngữ bài này</h3>
    <dl>
        <dt>APDU</dt><dd>Application Protocol Data Unit — đơn vị thông tin giữa terminal và card (ISO 7816-4).</dd>
        <dt>C-APDU / R-APDU</dt><dd>Command / Response APDU.</dd>
        <dt>CLA, INS, P1, P2</dt><dd>4 byte header bắt buộc.</dd>
        <dt>Lc, Le</dt><dd>Length of command/expected response. <code>Le = 0</code> trong wire = "tối đa".</dd>
        <dt>SW1-SW2</dt><dd>2 byte status word ở cuối R-APDU.</dd>
        <dt>Short APDU vs Extended APDU</dt><dd>Short: Lc/Le là 1 byte (tối đa 255/256). Extended: 3 byte (tối đa 65535/65536). EMV chủ yếu dùng short.</dd>
        <dt>T=0 / T=1</dt><dd>Hai giao thức truyền dữ liệu giữa contact card và reader (ISO 7816-3). T=0 byte-oriented, T=1 block-oriented.</dd>
        <dt>GET RESPONSE</dt><dd>Lệnh phụ trợ cho T=0, terminal phải gọi sau khi nhận <code>61 XX</code> để lấy data thật.</dd>
    </dl>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>Decode: <code>00 B2 02 14 00</code> — đọc record nào, SFI bao nhiêu?</li>
        <li>SW = <code>6A 82</code> nghĩa là gì? Khi nào bạn gặp nó?</li>
        <li>Tính P2 cho READ RECORD với SFI = 11.</li>
        <li>Tạo C-APDU SELECT AID của Mastercard (<code>A0000000041010</code>).</li>
        <li>Card trả <code>63 C1</code> — chuyện gì xảy ra?</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>C-APDU = CLA INS P1 P2 [Lc Data] [Le]; R-APDU = Data SW1 SW2 (luôn có SW).</li>
        <li>EMV chính chỉ dùng: SELECT, GPO, READ RECORD, INTERNAL AUTHENTICATE, GENERATE AC, VERIFY, GET DATA, GET RESPONSE.</li>
        <li>Cần thuộc các SW phổ biến (90 00, 61 XX, 63 CX, 6A 82, 6A 83, 6C XX, 69 82) để debug.</li>
        <li>READ RECORD: P1 = record number, P2 = (SFI &lt;&lt; 3) | 0x04.</li>
    </ul>
</div>
'''


# ============================================================
# LESSON 5: BER-TLV & EMV Tags
# ============================================================
LESSON_05 = '''
<div class="section">
    <h2>🎯 Mục tiêu bài học</h2>
    <ul>
        <li>Hiểu BER-TLV theo ISO/IEC 7816-4 (subset của ASN.1 BER).</li>
        <li>Phân biệt primitive tag vs constructed tag, biết cách encode tag 1-, 2-, 3- byte.</li>
        <li>Biết encode length (short form, long form).</li>
        <li>Thuộc bảng tag EMV thông dụng và biết tra cứu trong EMV Book 3 Annex A.</li>
        <li>Viết được TLV parser bằng Kotlin.</li>
    </ul>
</div>

<div class="section">
    <h2>📦 BER-TLV là gì?</h2>
    <p><strong>TLV</strong> = Tag – Length – Value. Mọi dữ liệu EMV được serialize bằng BER-TLV. "BER" = <em>Basic Encoding Rules</em>, là một quy tắc encoding của ASN.1 (ISO/IEC 8825-1). EMV dùng <strong>subset</strong> của BER (giới hạn ở ISO/IEC 7816-4).</p>

    <div class="diagram"><pre>
┌──────────┬──────────┬──────────────────┐
│   Tag    │  Length  │      Value       │
│  1-3 B   │  1-3 B*  │   0 – 65535 B    │
└──────────┴──────────┴──────────────────┘
   * EMV không dùng extended length > 3 bytes
    </pre></div>
</div>

<div class="section">
    <h2>🔍 Tag encoding</h2>
    <p>Tag là <strong>1, 2 hoặc 3 byte</strong>. Byte đầu tiên có ý nghĩa đặc biệt:</p>

    <div class="diagram"><pre>
Byte 1 của tag:
┌──────┬──────┬──────────────────────┐
│ b8b7 │  b6  │       b5 b4 b3 b2 b1 │
└──────┴──────┴──────────────────────┘
  class  P/C        tag number (5 bit)

Class (b8 b7):
  00 = Universal
  01 = Application      ← EMV dùng chủ yếu
  10 = Context-specific
  11 = Private          ← EMV cũng dùng

P/C (b6):
  0 = Primitive (value là raw data)
  1 = Constructed (value chứa TLV khác)

Tag number (b5..b1):
  Nếu khác 11111 (31) → tag là 1 byte
  Nếu  = 11111         → tag là multi-byte, các byte tiếp theo
                        có b8 = 1 cho byte trung gian,
                        b8 = 0 cho byte cuối.
    </pre></div>

    <h3>Ví dụ phân tích</h3>
    <table>
        <tr><th>Tag (hex)</th><th>Binary byte 1</th><th>Class</th><th>P/C</th><th>Số byte</th><th>Ghi chú</th></tr>
        <tr><td><code>5A</code></td><td>0101 1010</td><td>Application</td><td>Primitive</td><td>1</td><td>PAN</td></tr>
        <tr><td><code>5F 24</code></td><td>0101 1111</td><td>Application</td><td>Primitive</td><td>2</td><td>tag number = 11111 → byte tiếp = 0x24 = 36</td></tr>
        <tr><td><code>70</code></td><td>0111 0000</td><td>Application</td><td>Constructed</td><td>1</td><td>Record Template</td></tr>
        <tr><td><code>9F 02</code></td><td>1001 1111</td><td>Context-specific</td><td>Primitive</td><td>2</td><td>Amount Authorized</td></tr>
        <tr><td><code>BF 0C</code></td><td>1011 1111</td><td>Context-specific</td><td>Constructed</td><td>2</td><td>FCI Issuer Discretionary Data</td></tr>
    </table>

    <div class="info-box">
        <h3>💡 Quy tắc nhớ nhanh</h3>
        <ul>
            <li>Tag bắt đầu với <code>0x9F</code> → 2 byte, primitive.</li>
            <li>Tag bắt đầu với <code>0x5F</code> → 2 byte, primitive.</li>
            <li>Tag bắt đầu với <code>0xBF</code> → 2 byte, constructed.</li>
            <li>Mọi tag khác (<code>5A</code>, <code>70</code>, <code>82</code>...) → 1 byte.</li>
        </ul>
    </div>
</div>

<div class="section">
    <h2>📏 Length encoding</h2>

    <h3>Short form (1 byte)</h3>
    <p>Nếu length ≤ 127 → 1 byte, value chính là length.</p>
    <div class="code-block">Length = 8       →  <span class="hex">08</span>
Length = 127     →  <span class="hex">7F</span></div>

    <h3>Long form (2-3 byte)</h3>
    <p>Byte đầu có dạng <code>10000NNN</code>, trong đó NNN = số byte tiếp theo chứa length thực.</p>
    <div class="code-block">Length = 128     →  <span class="hex">81 80</span>
Length = 200     →  <span class="hex">81 C8</span>
Length = 256     →  <span class="hex">82 01 00</span>
Length = 500     →  <span class="hex">82 01 F4</span></div>

    <div class="warning-box">
        <h3>⚠️ Chú ý</h3>
        <p>Length encoding tuân chuẩn DER (definite, shortest form). <code>00</code> = "length là 0, value rỗng" — hợp lệ. Length <code>80</code> trong BER chuẩn nghĩa là "indefinite" — <strong>không được dùng trong EMV</strong>.</p>
    </div>
</div>

<div class="section">
    <h2>🪆 TLV lồng nhau (constructed)</h2>
    <p>Khi tag là constructed (bit b6 = 1), value <em>tự nó</em> là chuỗi TLV con. Ví dụ FCI:</p>

    <div class="code-block"><span class="hex">6F 1A
   84 07 A0 00 00 00 03 10 10
   A5 0F
      50 04 56 49 53 41
      87 01 01
      5F 2D 02 65 6E</span>

<span class="comment">// 6F (constructed) length 1A (26 byte). Value chứa:
//   84 (primitive) length 07 value = AID
//   A5 (constructed) length 0F (15 byte). Value chứa:
//     50 (primitive) length 04 value = "VISA"
//     87 (primitive) length 01 value = 01
//     5F2D (primitive) length 02 value = "en"</span></div>
</div>

<div class="section">
    <h2>🔢 Định dạng value</h2>
    <p>EMV Book 3 quy định mỗi tag có một <strong>data format</strong>. Phổ biến:</p>

    <table>
        <tr><th>Format</th><th>Ý nghĩa</th><th>Ví dụ</th></tr>
        <tr><td><strong>n</strong> (numeric)</td><td>BCD, mỗi nibble một chữ số 0-9, pad bằng F nếu lẻ</td><td>PAN <code>5A 08 45 32 12 34 56 78 90 10</code> = 4532123456789010</td></tr>
        <tr><td><strong>cn</strong></td><td>Compressed numeric — như n nhưng pad bằng F bên phải</td><td>PAN 17 số: <code>45 32 12 34 56 78 90 10 5F</code></td></tr>
        <tr><td><strong>an</strong></td><td>Alphanumeric — ASCII</td><td>"VISA" = <code>56 49 53 41</code></td></tr>
        <tr><td><strong>ans</strong></td><td>Alphanumeric + special — ASCII đầy đủ</td><td>Cardholder name "DOE/JOHN"</td></tr>
        <tr><td><strong>b</strong> (binary)</td><td>Raw byte</td><td>Cryptogram, key, signature</td></tr>
    </table>
</div>

<div class="section">
    <h2>📋 Danh sách EMV Tag thông dụng (EMV Book 3 Annex A)</h2>

    <h3>Card identification</h3>
    <table>
        <tr><th>Tag</th><th>Name</th><th>Format</th><th>Length</th></tr>
        <tr><td><code>4F</code></td><td>Application Identifier (AID)</td><td>b</td><td>5–16</td></tr>
        <tr><td><code>50</code></td><td>Application Label</td><td>ans</td><td>1–16</td></tr>
        <tr><td><code>57</code></td><td>Track 2 Equivalent Data</td><td>b</td><td>≤19</td></tr>
        <tr><td><code>5A</code></td><td>Application Primary Account Number (PAN)</td><td>cn</td><td>≤10</td></tr>
        <tr><td><code>5F20</code></td><td>Cardholder Name</td><td>ans</td><td>2–26</td></tr>
        <tr><td><code>5F24</code></td><td>Application Expiration Date</td><td>n6 (YYMMDD)</td><td>3</td></tr>
        <tr><td><code>5F25</code></td><td>Application Effective Date</td><td>n6</td><td>3</td></tr>
        <tr><td><code>5F28</code></td><td>Issuer Country Code</td><td>n3</td><td>2</td></tr>
        <tr><td><code>5F2A</code></td><td>Transaction Currency Code</td><td>n3</td><td>2</td></tr>
        <tr><td><code>5F2D</code></td><td>Language Preference</td><td>an2</td><td>2–8</td></tr>
        <tr><td><code>5F30</code></td><td>Service Code</td><td>n3</td><td>2</td></tr>
        <tr><td><code>5F34</code></td><td>PAN Sequence Number</td><td>n2</td><td>1</td></tr>
    </table>

    <h3>Templates (constructed)</h3>
    <table>
        <tr><th>Tag</th><th>Name</th></tr>
        <tr><td><code>6F</code></td><td>File Control Information (FCI) Template</td></tr>
        <tr><td><code>70</code></td><td>READ RECORD Response Message Template</td></tr>
        <tr><td><code>77</code></td><td>Response Message Template Format 2</td></tr>
        <tr><td><code>80</code></td><td>Response Message Template Format 1</td></tr>
        <tr><td><code>A5</code></td><td>FCI Proprietary Template</td></tr>
        <tr><td><code>BF0C</code></td><td>FCI Issuer Discretionary Data</td></tr>
    </table>

    <h3>Application / Transaction</h3>
    <table>
        <tr><th>Tag</th><th>Name</th></tr>
        <tr><td><code>82</code></td><td>Application Interchange Profile (AIP)</td></tr>
        <tr><td><code>84</code></td><td>Dedicated File (DF) Name</td></tr>
        <tr><td><code>87</code></td><td>Application Priority Indicator</td></tr>
        <tr><td><code>88</code></td><td>SFI of the Directory EF</td></tr>
        <tr><td><code>8C</code></td><td>CDOL1</td></tr>
        <tr><td><code>8D</code></td><td>CDOL2</td></tr>
        <tr><td><code>8E</code></td><td>CVM List</td></tr>
        <tr><td><code>8F</code></td><td>Certification Authority Public Key Index</td></tr>
        <tr><td><code>90</code></td><td>Issuer Public Key Certificate</td></tr>
        <tr><td><code>92</code></td><td>Issuer Public Key Remainder</td></tr>
        <tr><td><code>93</code></td><td>Signed Static Application Data</td></tr>
        <tr><td><code>94</code></td><td>Application File Locator (AFL)</td></tr>
        <tr><td><code>95</code></td><td>Terminal Verification Results (TVR)</td></tr>
        <tr><td><code>97</code></td><td>Transaction Certificate Data Object List (TDOL)</td></tr>
        <tr><td><code>9A</code></td><td>Transaction Date</td></tr>
        <tr><td><code>9B</code></td><td>Transaction Status Information (TSI)</td></tr>
        <tr><td><code>9C</code></td><td>Transaction Type</td></tr>
    </table>

    <h3>Terminal data (Context-specific, 9F xx)</h3>
    <table>
        <tr><th>Tag</th><th>Name</th></tr>
        <tr><td><code>9F02</code></td><td>Amount, Authorized (n12)</td></tr>
        <tr><td><code>9F03</code></td><td>Amount, Other (n12)</td></tr>
        <tr><td><code>9F09</code></td><td>Application Version Number (terminal)</td></tr>
        <tr><td><code>9F10</code></td><td>Issuer Application Data (IAD)</td></tr>
        <tr><td><code>9F12</code></td><td>Application Preferred Name</td></tr>
        <tr><td><code>9F13</code></td><td>Last Online ATC Register</td></tr>
        <tr><td><code>9F17</code></td><td>PIN Try Counter</td></tr>
        <tr><td><code>9F1A</code></td><td>Terminal Country Code (n3)</td></tr>
        <tr><td><code>9F1E</code></td><td>IFD Serial Number</td></tr>
        <tr><td><code>9F26</code></td><td>Application Cryptogram (8 byte)</td></tr>
        <tr><td><code>9F27</code></td><td>Cryptogram Information Data (CID)</td></tr>
        <tr><td><code>9F32</code></td><td>Issuer Public Key Exponent</td></tr>
        <tr><td><code>9F33</code></td><td>Terminal Capabilities (3 byte)</td></tr>
        <tr><td><code>9F34</code></td><td>CVM Results (3 byte)</td></tr>
        <tr><td><code>9F35</code></td><td>Terminal Type</td></tr>
        <tr><td><code>9F36</code></td><td>Application Transaction Counter (ATC, 2 byte)</td></tr>
        <tr><td><code>9F37</code></td><td>Unpredictable Number (4 byte)</td></tr>
        <tr><td><code>9F38</code></td><td>PDOL</td></tr>
        <tr><td><code>9F40</code></td><td>Additional Terminal Capabilities (5 byte)</td></tr>
        <tr><td><code>9F42</code></td><td>Application Currency Code</td></tr>
        <tr><td><code>9F44</code></td><td>Application Currency Exponent</td></tr>
        <tr><td><code>9F46</code></td><td>ICC Public Key Certificate</td></tr>
        <tr><td><code>9F47</code></td><td>ICC Public Key Exponent</td></tr>
        <tr><td><code>9F48</code></td><td>ICC Public Key Remainder</td></tr>
        <tr><td><code>9F4A</code></td><td>SDA Tag List</td></tr>
        <tr><td><code>9F4B</code></td><td>Signed Dynamic Application Data</td></tr>
        <tr><td><code>9F66</code></td><td>Terminal Transaction Qualifiers (TTQ)</td></tr>
    </table>
</div>

<div class="section">
    <h2>🔬 Ví dụ parse một READ RECORD response</h2>
    <div class="code-block"><span class="hex">70 30
   5A 08 45 32 12 34 56 78 90 10
   5F 24 03 27 12 31
   5F 25 03 22 01 01
   5F 28 02 07 04
   5F 34 01 01
   57 13 45 32 12 34 56 78 90 10 D2 71 22 01 00 01 23 45 67 89 0F</span>

<span class="comment">// Parse:</span>
70 (constructed) length 30 (48 byte) — Record Template
  ├─ 5A (PAN)         len 08 = <span class="hex">45 32 12 34 56 78 90 10</span> → 4532 1234 5678 9010
  ├─ 5F24 (Expiry)    len 03 = <span class="hex">27 12 31</span>             → 2027-12-31
  ├─ 5F25 (Effective) len 03 = <span class="hex">22 01 01</span>             → 2022-01-01
  ├─ 5F28 (Country)   len 02 = <span class="hex">07 04</span>                → 0704 = VN
  ├─ 5F34 (PAN Seq)   len 01 = <span class="hex">01</span>                  → 1
  └─ 57 (Track 2 eq)  len 13 = <span class="hex">45 32 12 34 56 78 90 10 D2 71 22 01 00 01 23 45 67 89 0F</span>
       └ Track 2: PAN '45321234567890 10' + 'D' + expiry '2712' + svc '201' + discretionary '0001234567890F'</div>
</div>

<div class="section">
    <h2>📱 Kotlin TLV parser</h2>
    <div class="code-block">data class Tlv(val tag: Int, val value: ByteArray, val children: List&lt;Tlv&gt; = emptyList()) {
    val isConstructed get() = (tag.bytesOf().first().toInt() and 0x20) != 0
}

class TlvParser(private val data: ByteArray) {
    private var pos = 0

    fun parseAll(): List&lt;Tlv&gt; {
        val list = mutableListOf&lt;Tlv&gt;()
        while (pos &lt; data.size) {
            <span class="comment">// Skip BER padding (00 hoặc FF)</span>
            if (data[pos] == 0x00.toByte() || data[pos] == 0xFF.toByte()) { pos++; continue }
            list += readOne()
        }
        return list
    }

    private fun readOne(): Tlv {
        val tag = readTag()
        val len = readLength()
        val value = data.copyOfRange(pos, pos + len); pos += len
        val constructed = (tag.bytesOf().first().toInt() and 0x20) != 0
        val children = if (constructed) TlvParser(value).parseAll() else emptyList()
        return Tlv(tag, value, children)
    }

    private fun readTag(): Int {
        val first = data[pos++].toInt() and 0xFF
        var tag = first
        if ((first and 0x1F) == 0x1F) {              <span class="comment">// multi-byte tag</span>
            do {
                val next = data[pos++].toInt() and 0xFF
                tag = (tag shl 8) or next
            } while ((tag and 0x80) != 0 && (data[pos - 1].toInt() and 0x80) != 0)
        }
        return tag
    }

    private fun readLength(): Int {
        val first = data[pos++].toInt() and 0xFF
        if (first &lt; 0x80) return first
        val numBytes = first and 0x7F
        var len = 0
        repeat(numBytes) { len = (len shl 8) or (data[pos++].toInt() and 0xFF) }
        return len
    }
}

fun Int.bytesOf(): ByteArray {
    val bytes = mutableListOf&lt;Byte&gt;()
    var v = this
    while (v != 0) { bytes.add(0, (v and 0xFF).toByte()); v = v ushr 8 }
    return bytes.toByteArray()
}

<span class="comment">// Helper tìm tag (depth-first)</span>
fun List&lt;Tlv&gt;.findTag(tag: Int): Tlv? {
    for (t in this) {
        if (t.tag == tag) return t
        t.children.findTag(tag)?.let { return it }
    }
    return null
}</div>
</div>

<div class="term-box">
    <h3>📘 Thuật ngữ bài này</h3>
    <dl>
        <dt>BER-TLV</dt><dd>Basic Encoding Rules cho Tag-Length-Value, là subset của ASN.1 (ISO 8825). EMV chuẩn hóa subset của BER trong ISO 7816-4.</dd>
        <dt>Primitive vs Constructed</dt><dd>Primitive: value là raw data. Constructed: value chứa các TLV con. Bit b6 byte đầu của tag = 1 → constructed.</dd>
        <dt>Short / Long form length</dt><dd>Short: 1 byte (≤127). Long: byte đầu 81/82/… cho biết có 1/2/… byte tiếp theo chứa length.</dd>
        <dt>BCD / cn / n format</dt><dd>n = numeric BCD (mỗi nibble một chữ số). cn = compressed numeric (pad F bên phải).</dd>
        <dt>PDOL / CDOL1 / CDOL2 / DDOL / TDOL</dt><dd>Các "Data Object List" — chỉ chứa danh sách (tag, length), terminal phải nhồi data theo thứ tự.</dd>
        <dt>Template</dt><dd>Tag constructed chứa các TLV khác. EMV dùng: 6F, 70, 77, 80, A5, BF0C, 9F69…</dd>
    </dl>
</div>

<div class="exercise">
    <h3>🧪 Bài tập</h3>
    <ol>
        <li>Encode TLV cho tag <code>5F24</code> (expiry) ngày 31/12/2028.</li>
        <li>Length = 130 → encode ra mấy byte? Hex bằng bao nhiêu?</li>
        <li>Tag <code>9F26</code> là primitive hay constructed? Vì sao?</li>
        <li>Parse: <code>9F02 06 00 00 00 01 50 00</code> — amount là bao nhiêu (VND, biết exponent = 0)?</li>
        <li>Cài thử <code>TlvParser</code> ở trên và parse FCI của Mastercard.</li>
    </ol>
</div>

<div class="success-box">
    <h3>✅ Tóm tắt</h3>
    <ul>
        <li>BER-TLV: Tag (1-3 byte) + Length (1-3 byte) + Value (raw hoặc TLV con).</li>
        <li>Tag bắt đầu <code>5F/9F/BF</code> → 2 byte; <code>BF/A5/6F/70/77</code> → constructed.</li>
        <li>Length: short form ≤127; long form <code>81 XX</code>, <code>82 XX XX</code>.</li>
        <li>EMV Book 3 Annex A chứa toàn bộ tag — luôn tra spec gốc trước khi đoán.</li>
    </ul>
</div>
'''

