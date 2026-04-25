using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using StudyBuilder.Adapter.Services;
using StudyBuilder.Adapter.Transformers;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((hostContext, services) =>
    {
        // Register services
        services.AddHttpClient();
        services.AddSingleton<IStudyBuilderService, StudyBuilderService>();
        services.AddSingleton<ISdrApiService, SdrApiService>();
        services.AddSingleton<IUsdmTransformer, UsdmTransformer>();
        
        // Register hosted service
        services.AddHostedService<StudyBuilderAdapterService>();
    })
    .Build();

await host.RunAsync();
