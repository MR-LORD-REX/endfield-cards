export const sections = [
  {
    title: "Start here",
    pages: [
      { id: "overview", title: "Overview", path: "overview.md", description: "Create Endfield cards with EF_Cards and an injected SKPORT client." },
      { id: "gallery", title: "Gallery", path: "gallery.md", description: "Browse all 25 implemented card templates and open full-size PNG examples." },
      { id: "getting-started/installation", title: "Installation", path: "getting-started/installation.md", description: "Install endfield-cards and prepare your first request." },
      { id: "getting-started/quickstart", title: "Quickstart", path: "getting-started/quickstart.md", description: "Fetch, create and save your first profile and character cards." },
    ],
  },
  {
    title: "Guides",
    pages: [
      { id: "guides/configuration", title: "Configuration", path: "guides/configuration.md", description: "Set language, output format, timezone and caching once." },
      { id: "guides/artwork", title: "Custom artwork", path: "guides/artwork.md", description: "Choose local or remote artwork and fit it to character cards." },
      { id: "guides/card-results", title: "Card results", path: "guides/card-results.md", description: "Save images, handle pages and use the returned data and selectors." },
      { id: "guides/errors", title: "Errors", path: "guides/errors.md", description: "Handle invalid templates, fetch failures and unavailable pulls or wiki cards." },
    ],
  },
  {
    title: "Cards",
    pages: [
      { id: "cards/profile", title: "Profile", path: "cards/profile.md", description: "Create a public or owner profile card with one of three templates." },
      { id: "cards/character", title: "Character", path: "cards/character.md", description: "Select an operator and create a build card with one of four templates." },
      { id: "cards/compare", title: "Compare", path: "cards/compare.md", description: "Compare two operator builds with stats, weapons, equipment and talents." },
      { id: "cards/roster", title: "All characters", path: "cards/roster.md", description: "Create an authenticated owner's complete roster card." },
      { id: "cards/live", title: "Live status", path: "cards/live.md", description: "Show live activity, resource meters and recovery times." },
      { id: "cards/factory", title: "Factory & Dijiang", path: "cards/factory.md", description: "Show factory funds, settlements, Dijiang cabins and crew." },
      { id: "cards/exploration", title: "Exploration", path: "cards/exploration.md", description: "Show exploration across all supplied regions, areas and categories." },
      { id: "cards/monument", title: "Monument", path: "cards/monument.md", description: "Create a Monument overview or a detailed event card with battle teams." },
      { id: "cards/contingency-contract", title: "Contingency Contract", path: "cards/contingency-contract.md", description: "Create contract overview or detailed battle-record cards." },
    ],
  },
  {
    title: "Reference",
    pages: [
      { id: "reference/client", title: "EF_Cards", path: "reference/client.md", description: "Client construction, methods, parameters, return values and resource ownership." },
      { id: "reference/templates", title: "Templates", path: "reference/templates.md", description: "Choose stable numeric templates and browse the available variants." },
      { id: "attribution", title: "Attribution", path: "attribution.md", description: "UI references, Hypergryph game assets, project license and attribution." },
    ],
  },
];

export const pages = sections.flatMap((section) => section.pages.map((page) => ({ ...page, section: section.title })));
