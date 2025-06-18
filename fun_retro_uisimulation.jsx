import { useState } from "react";
import { QRCodeSVG } from "qrcode.react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { CheckCircle2, Star, ThumbsDown, Lightbulb } from "lucide-react";

/**
 * FunRetroUISimulation.jsx
 * ------------------------------------------------------
 * A lightweight proof‑of‑concept UI that walks a participant
 * through a QR‑based, themed retrospective and (mock) pushes
 * the captured feedback to Jira when they hit “Save”.
 *
 * 👉  How it works
 *      1.  Participant scans the presented QR code (simulated here).
 *      2.  Chooses a fun theme for the session (e.g. Cricket).
 *      3.  Answers the classic retro triad (Went Well / Didn’t / Improve).
 *      4.  On “Save”, feedback is bundled and—via mock API—sent to Jira
 *          (replace with your own endpoint to go live).
 *      5.  A confirmation screen shows the created ticket key.
 *
 *  Tech highlights
 *      •  Tailwind‑powered responsive layout (mobile‑first).
 *      •  shadcn/ui components for clean cards & buttons.
 *      •  lucide‑react icons for quick visual cues.
 *      •  qrcode.react to generate an on‑the‑fly QR code.
 */

export default function FunRetroApp() {
  const [step, setStep] = useState(0);
  const [theme, setTheme] = useState(null);
  const [answers, setAnswers] = useState({ good: "", bad: "", improve: "" });
  const [ticketKey, setTicketKey] = useState(null);

  const themes = [
    {
      id: "cricket",
      name: "Cricket Fever",
      accent: "bg-green-600",
      questions: {
        good: "Which shots hit the boundary? (What went well)",
        bad: "Where did we lose wickets? (What didn't go well)",
        improve: "How can we level up our next innings? (Improvements)"
      }
    },
    {
      id: "south",
      name: "South Cinema",
      accent: "bg-red-600",
      questions: {
        good: "Which scenes got whistles?",
        bad: "Which plot holes bored the crowd?",
        improve: "What twist will make the sequel blockbuster?"
      }
    },
    {
      id: "space",
      name: "Space Odyssey",
      accent: "bg-indigo-600",
      questions: {
        good: "Which thrusters fired flawlessly?",
        bad: "Where did we burn extra fuel?",
        improve: "What upgrades ensure a smoother orbit?"
      }
    }
  ];

  const handleSubmit = async () => {
    setStep(3);
    // Simulate network + Jira create
    const mockCreateJiraTicket = (payload) =>
      new Promise((res) => setTimeout(() => res({ key: "RET-123" }), 1500));
    const { key } = await mockCreateJiraTicket({ theme, answers });
    setTicketKey(key);
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardContent className="p-6 space-y-6">
          {/* Step indicators */}
          <div className="flex items-center justify-between text-sm font-medium text-gray-400">
            {['Scan','Theme','Feedback','Done'].map((label,i)=>(
              <div key={label} className={`flex-1 text-center ${step>=i?'text-primary':''}`}>{label}</div>
            ))}
          </div>

          {step === 0 && (
            <div className="flex flex-col items-center space-y-4">
              <QRCodeSVG value="https://funretro.company/retro/session/abc" size={180} />
              <p className="text-center text-gray-600">Scan to open the retro on your phone</p>
              <Button onClick={() => setStep(1)}>I’ve scanned it</Button>
            </div>
          )}

          {step === 1 && (
            <div className="space-y-4">
              <p className="font-semibold text-center">Pick a vibe for today</p>
              <div className="grid grid-cols-1 gap-3">
                {themes.map((t) => (
                  <button
                    key={t.id}
                    onClick={() => {
                      setTheme(t);
                      setStep(2);
                    }}
                    className={`rounded-xl p-4 border flex items-center gap-3 shadow-sm hover:shadow-md transition ${t.accent}/20`}
                  >
                    <span className={`${t.accent} w-10 h-10 rounded-full flex items-center justify-center text-white font-bold`}>{t.name.charAt(0)}</span>
                    <span className="font-medium flex-1 text-left">{t.name}</span>
                    <Star className="text-yellow-500" size={18} />
                  </button>
                ))}
              </div>
            </div>
          )}

          {step === 2 && theme && (
            <div className="space-y-6">
              <p className="font-semibold text-center">{theme.name}</p>

              <div className="space-y-4">
                <QuestionBlock
                  icon={<CheckCircle2 className="text-green-600" />}
                  label={theme.questions.good}
                  value={answers.good}
                  onChange={(e) => setAnswers({ ...answers, good: e.target.value })}
                />
                <QuestionBlock
                  icon={<ThumbsDown className="text-red-600" />}
                  label={theme.questions.bad}
                  value={answers.bad}
                  onChange={(e) => setAnswers({ ...answers, bad: e.target.value })}
                />
                <QuestionBlock
                  icon={<Lightbulb className="text-yellow-500" />}
                  label={theme.questions.improve}
                  value={answers.improve}
                  onChange={(e) => setAnswers({ ...answers, improve: e.target.value })}
                />
              </div>

              <Button className="w-full" onClick={handleSubmit}>Save & Push to Jira</Button>
            </div>
          )}

          {step === 3 && (
            <div className="flex flex-col items-center space-y-4">
              {ticketKey ? (
                <>
                  <CheckCircle2 size={48} className="text-green-600" />
                  <p className="text-xl font-semibold text-center">Feedback saved!</p>
                  <p className="text-gray-600 text-center">Created Jira ticket <span className="font-medium text-primary">{ticketKey}</span></p>
                  <Button variant="secondary" onClick={()=>{setStep(0);setTheme(null);setAnswers({good:'',bad:'',improve:''});}}>Start New Retro</Button>
                </>
              ) : (
                <p className="text-gray-600">Submitting…</p>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function QuestionBlock({ icon, label, value, onChange }) {
  return (
    <div className="space-y-2">
      <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
        {icon}
        {label}
      </label>
      <Textarea
        rows={2}
        value={value}
        onChange={onChange}
        className="resize-none"
        placeholder="Your thoughts…"
      />
    </div>
  );
}
