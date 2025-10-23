import { FileText, Search, MessageSquare, Shield } from "lucide-react";

export function WelcomeScreen() {
  const features = [
    {
      icon: FileText,
      title: "Complex Documents Simplified",
      description: "Navigate hundreds of pages of health plan PDFs with ease",
    },
    {
      icon: Search,
      title: "Instant Answers",
      description: "Get quick, accurate answers about your benefits and coverage",
    },
    {
      icon: MessageSquare,
      title: "Natural Conversation",
      description: "Ask questions in plain language, just like talking to an expert",
    },
    {
      icon: Shield,
      title: "Trusted & Reliable",
      description: "Information sourced directly from your official plan documents",
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center space-y-8 animate-fade-in">
      <div className="space-y-4">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-primary to-accent shadow-lg">
          <FileText className="w-10 h-10 text-primary-foreground" />
        </div>
        <h2 className="text-3xl font-bold text-foreground">
          Welcome to PSIP Navigator
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Your health plan benefits information lives in hundreds of pages of PDFs.
          We help you navigate it easily with AI-powered assistance.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl w-full mt-8">
        {features.map((feature, index) => (
          <div
            key={index}
            className="bg-card border border-border rounded-xl p-6 text-left hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <feature.icon className="w-8 h-8 text-primary mb-3" />
            <h3 className="font-semibold text-foreground mb-2">{feature.title}</h3>
            <p className="text-sm text-muted-foreground">{feature.description}</p>
          </div>
        ))}
      </div>

      <div className="pt-6">
        <p className="text-sm text-muted-foreground">
          Start by asking a question about your health plan benefits below
        </p>
      </div>
    </div>
  );
}
