using EDC.Adapter.Services;
using EDC.Adapter.Transformers;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((hostContext, services) =>
    {
        // Register services
        services.AddHttpClient();
        services.AddSingleton<ISdrApiService, SdrApiService>();
        services.AddSingleton<IEdcService, EdcService>();
        services.AddSingleton<IFormGenerator, FormGenerator>();
        
        // Register hosted service
        services.AddHostedService<EdcAdapterService>();
    })
    .Build();

await host.RunAsync();
